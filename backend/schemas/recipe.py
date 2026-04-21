from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


class RecipeCreate(BaseModel):
    title: str
    ingredients: str          
    steps: str
    image_url: Optional[str] = None  # URL to recipe image
    meal_type: Optional[str] = None
    dietary_focus: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title must not be empty")
        return v.strip()

    @field_validator("ingredients")
    @classmethod
    def ingredients_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Ingredients must not be empty")
        return v.strip()

    @field_validator("meal_type")
    @classmethod
    def validate_meal_type(cls, v):
        allowed = {"Breakfast", "Lunch", "Dinner", "Snack", None}
        if v and v not in allowed:
            raise ValueError(f"meal_type must be one of {allowed - {None}}")
        return v

    @field_validator("dietary_focus")
    @classmethod
    def validate_dietary_focus(cls, v):
        allowed = {"High Protein", "High Carb", "Balanced", "Low Calorie", None}
        if v and v not in allowed:
            raise ValueError(f"dietary_focus must be one of {allowed - {None}}")
        return v


class RecipeResponse(BaseModel):
    id: int
    title: str
    ingredients: str
    steps: str
    image_url: Optional[str]
    meal_type: Optional[str]
    dietary_focus: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class RecommendationRequest(BaseModel):
    ingredients: List[str]
    top_k: Optional[int] = 5

    @field_validator("ingredients")
    @classmethod
    def ingredients_not_empty(cls, v):
        if not v:
            raise ValueError("Provide at least one ingredient")
        return [i.strip().lower() for i in v if i.strip()]


class RecommendationResult(BaseModel):
    recipe: RecipeResponse
    match_count: int
    match_score: float
    missing_ingredients: List[str]
    substitutions: dict


class ExportFormat(BaseModel):
    format: str = "markdown"   # "markdown" or "pdf"
