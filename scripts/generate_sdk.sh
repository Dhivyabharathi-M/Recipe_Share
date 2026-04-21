#!/usr/bin/env bash
# generate_sdk.sh – Generate Python SDK from the live OpenAPI spec

echo "============================================"
echo "  Generating RecipeShare Python SDK"
echo "============================================"
echo ""
echo "Prerequisites:"
echo "  • Node.js installed (npm available)"
echo "  • Backend running on http://localhost:8000"
echo ""

# Install generator CLI globally if not already present
if ! command -v openapi-generator-cli &>/dev/null; then
  echo "Installing OpenAPI Generator CLI..."
  npm install -g @openapitools/openapi-generator-cli
fi

# Generate SDK
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g python \
  -o recipe_sdk \
  --package-name recipe_sdk

echo ""
echo "SDK generated at ./recipe_sdk"
echo ""
echo "Install the SDK:"
echo "  cd recipe_sdk && pip install -e ."
echo ""
echo "Usage example:"
cat <<'EXAMPLE'
from recipe_sdk.api.recipes_api import RecipesApi
from recipe_sdk import ApiClient, Configuration

config = Configuration(host="http://localhost:8000")
client = ApiClient(configuration=config)
api    = RecipesApi(client)

# List all recipes
recipes = api.list_recipes_recipes_get()
for r in recipes:
    print(r.title, "|", r.dietary_focus)

# Add a recipe
from recipe_sdk.models.recipe_create import RecipeCreate
new_recipe = RecipeCreate(
    title="Garlic Bread",
    ingredients="bread, garlic, butter, parsley",
    steps="1. Mix garlic and butter. 2. Spread on bread. 3. Bake at 180°C for 10 min."
)
result = api.create_recipe_recipes_post(new_recipe)
print("Created:", result.id, result.title)
EXAMPLE
