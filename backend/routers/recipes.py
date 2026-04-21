from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional

from models.database import get_db, Recipe
from schemas.recipe import RecipeCreate, RecipeResponse, RecommendationResult
from services.recommendation import (
    auto_tag_dietary, get_meal_type_by_time, recommend_recipes
)
from services.export import export_as_markdown, export_as_pdf
from services.websocket_manager import manager

router = APIRouter()


# ── POST /recipes/ ─────────────────────────────────────────────────────────────
@router.post("/recipes/", response_model=RecipeResponse, status_code=201,
             tags=["Recipes"])
async def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)):
    # Auto-tag dietary focus if not provided
    dietary = payload.dietary_focus or auto_tag_dietary(payload.ingredients)
    meal    = payload.meal_type    or get_meal_type_by_time()

    recipe = Recipe(
        title         = payload.title,
        ingredients   = payload.ingredients,
        steps         = payload.steps,
        image_url     = payload.image_url,
        meal_type     = meal,
        dietary_focus = dietary,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    # Broadcast via WebSocket
    await manager.broadcast({
        "event": "new_recipe",
        "id":    recipe.id,
        "title": recipe.title,
        "message": f"New recipe added: {recipe.title}",
    })

    return recipe


# ── GET /recipes/ ──────────────────────────────────────────────────────────────
@router.get("/recipes/", response_model=List[RecipeResponse], tags=["Recipes"])
def list_recipes(
    skip: int = 0,
    limit: int = Query(default=50, le=200),
    meal_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Recipe)
    if meal_type:
        q = q.filter(Recipe.meal_type == meal_type)
    return q.offset(skip).limit(limit).all()


# ── GET /recipes/{id} ─────────────────────────────────────────────────────────
@router.get("/recipes/{recipe_id}", response_model=RecipeResponse, tags=["Recipes"])
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# ── PUT /recipes/{id} ──────────────────────────────────────────────────────────
@router.put("/recipes/{recipe_id}", response_model=RecipeResponse, tags=["Recipes"])
async def update_recipe(recipe_id: int, payload: RecipeCreate, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe.title          = payload.title
    recipe.ingredients    = payload.ingredients
    recipe.steps          = payload.steps
    recipe.image_url      = payload.image_url
    recipe.meal_type      = payload.meal_type or auto_tag_dietary(payload.ingredients)
    recipe.dietary_focus  = payload.dietary_focus or get_meal_type_by_time()
    
    db.commit()
    db.refresh(recipe)
    
    # Broadcast update via WebSocket
    await manager.broadcast({
        "event": "recipe_updated",
        "id":    recipe.id,
        "title": recipe.title,
        "message": f"Recipe updated: {recipe.title}",
    })
    
    return recipe

# ── DELETE /recipes/{id} ──────────────────────────────────────────────────────
@router.delete("/recipes/{recipe_id}", status_code=204, tags=["Recipes"])
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()


# ── GET /recipes/{id}/export ──────────────────────────────────────────────────
@router.get("/recipes/{recipe_id}/export", tags=["Recipes"])
def export_recipe(
    recipe_id: int,
    format: str = Query(default="markdown", pattern="^(markdown|pdf)$"),
    db: Session = Depends(get_db),
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if format == "pdf":
        pdf_bytes = export_as_pdf(recipe)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{recipe.title}.pdf"'},
        )

    md = export_as_markdown(recipe)
    return Response(
        content=md,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{recipe.title}.md"'},
    )


# ── GET /recommendations/ ─────────────────────────────────────────────────────
@router.get("/recommendations/", response_model=List[RecommendationResult],
            tags=["Recommendations"])
def get_recommendations(
    ingredients: str = Query(..., description="Comma-separated ingredients"),
    top_k: int = Query(default=5, ge=1, le=20),
    time_based: bool = Query(default=False,
                             description="Filter by current time of day"),
    db: Session = Depends(get_db),
):
    if not ingredients.strip():
        raise HTTPException(status_code=422, detail="Ingredients cannot be empty")

    user_ingredients = [i.strip() for i in ingredients.split(",") if i.strip()]
    meal_filter      = get_meal_type_by_time() if time_based else None
    all_recipes      = db.query(Recipe).all()

    results = recommend_recipes(user_ingredients, all_recipes, top_k, meal_filter)
    return results


# ── GET /stats/ ───────────────────────────────────────────────────────────────
@router.get("/stats/", tags=["Stats"])
def get_stats(db: Session = Depends(get_db)):
    """Returns ingredient category breakdown for charts."""
    from services.recommendation import PROTEIN_KEYWORDS, CARB_KEYWORDS
    recipes = db.query(Recipe).all()
    protein_count = 0
    carb_count    = 0
    balanced      = 0
    low_cal       = 0
    for r in recipes:
        focus = r.dietary_focus or ""
        if focus == "High Protein":   protein_count += 1
        elif focus == "High Carb":    carb_count    += 1
        elif focus == "Balanced":     balanced      += 1
        else:                         low_cal       += 1

    return {
        "total": len(recipes),
        "breakdown": {
            "High Protein": protein_count,
            "High Carb":    carb_count,
            "Balanced":     balanced,
            "Low Calorie":  low_cal,
        },
        "meal_types": {
            mt: sum(1 for r in recipes if r.meal_type == mt)
            for mt in ["Breakfast", "Lunch", "Dinner", "Snack"]
        },
    }
