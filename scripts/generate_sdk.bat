@echo off
echo ============================================
echo   Generating RecipeShare Python SDK
echo ============================================
echo.
echo Make sure the backend is running on http://localhost:8000
echo.

where openapi-generator-cli >nul 2>&1
if errorlevel 1 (
  echo Installing OpenAPI Generator CLI...
  npm install -g @openapitools/openapi-generator-cli
)

openapi-generator-cli generate ^
  -i http://localhost:8000/openapi.json ^
  -g python ^
  -o recipe_sdk ^
  --package-name recipe_sdk

echo.
echo SDK generated at .\recipe_sdk
echo Install with: cd recipe_sdk && pip install -e .
