from datetime import datetime
from typing import List, Dict, Tuple
from models.database import Recipe

# Ingredient normalization 
def normalize_ingredient(ingredient: str) -> str:
    """Normalize ingredient names to handle singular/plural forms."""
    ing = ingredient.lower().strip()
    
    # Common singular/plural mappings
    singular_map = {
        "eggs": "egg",
        "tomatoes": "tomato",
        "onions": "onion",
        "garlic": "garlic",  
        "potatoes": "potato",
        "peppers": "pepper",
        "mushrooms": "mushroom",
        "carrots": "carrot",
        "beans": "bean",
        "lentils": "lentil",
        "noodles": "noodle",
        "olives": "olive",
        "berries": "berry",
        "nuts": "nut",
        "seeds": "seed",
    }
    
    return singular_map.get(ing, ing)


# Nutritional auto-tagging 
PROTEIN_KEYWORDS = {"chicken", "egg", "tofu", "lentil",
                    "beef", "fish", "tuna", "salmon", "turkey", "shrimp", "paneer"}
CARB_KEYWORDS    = {"rice", "pasta", "bread", "potato", "noodle",
                    "oats", "quinoa", "flour", "tortilla", "couscous"}

def auto_tag_dietary(ingredients_str: str) -> str:
    ingredients = {normalize_ingredient(i.strip()) for i in ingredients_str.split(",")}
    has_protein = bool(ingredients & PROTEIN_KEYWORDS)
    has_carb    = bool(ingredients & CARB_KEYWORDS)
    if has_protein and has_carb:
        return "Balanced"
    if has_protein:
        return "High Protein"
    if has_carb:
        return "High Carb"
    return "Low Calorie"


# Time-based meal type
def get_meal_type_by_time() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "Breakfast"
    if 11 <= hour < 15:
        return "Lunch"
    if 18 <= hour < 21:
        return "Dinner"
    return "Snack"


#  Smart substitution dictionary 
SUBSTITUTIONS: Dict[str, str] = {
    "pine nut":      "walnuts",
    "butter":         "olive oil or coconut oil",
    "milk":           "almond milk or oat milk",
    "cream":          "coconut cream or Greek yogurt",
    "parmesan":       "pecorino romano or cheddar",
    "breadcrumb":    "crushed crackers or panko",
    "sour cream":     "Greek yogurt or cottage cheese",
    "heavy cream":    "evaporated milk or coconut cream",
    "bacon":          "turkey bacon or tempeh",
    "beef":           "chicken or plant-based meat",
    "pasta":          "zucchini noodles or rice noodles",
    "sugar":          "honey or maple syrup",
    "flour":          "almond flour or coconut flour",
    "egg":            "flax eggs (1 tbsp ground flax + 3 tbsp water per egg)",
}

def get_substitutions(missing: List[str]) -> Dict[str, str]:
    result = {}
    for item in missing:
        key = item.lower().strip()
        if key in SUBSTITUTIONS:
            result[item] = SUBSTITUTIONS[key]
    return result


# Core recommendation engine
def recommend_recipes(
    user_ingredients: List[str],
    recipes: List[Recipe],
    top_k: int = 5,
    filter_meal_type: str = None,
) -> List[Dict]:
    # Normalize user ingredients
    user_set = {normalize_ingredient(i.strip()) for i in user_ingredients}

    scored = []
    for recipe in recipes:
        # Normalize recipe ingredients
        recipe_ingredients = {
            normalize_ingredient(i.strip()) for i in recipe.ingredients.split(",")
        }
        matched   = user_set & recipe_ingredients
        missing   = recipe_ingredients - user_set
        match_cnt = len(matched)
        score     = round(match_cnt / max(len(recipe_ingredients), 1) * 100, 2)

        if match_cnt == 0:
            continue

        # Time-based filter (optional, only if caller passes filter_meal_type)
        if filter_meal_type and recipe.meal_type and recipe.meal_type != filter_meal_type:
            continue

        scored.append({
            "recipe":               recipe,
            "match_count":          match_cnt,
            "match_score":          score,
            "missing_ingredients":  list(missing),
            "substitutions":        get_substitutions(list(missing)),
        })

    scored.sort(key=lambda x: x["match_count"], reverse=True)
    return scored[:top_k]
