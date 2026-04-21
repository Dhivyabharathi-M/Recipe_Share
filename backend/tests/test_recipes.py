import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# conftest.py has already patched models.database to use the test engine.
# Import order matters: conftest runs first via pytest collection.
from fastapi.testclient import TestClient
from tests.conftest import TestingSession
from models.database import get_db
from main import app


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ── Helper ─────────────────────────────────────────────────────────────────────
def create_sample_recipe(**kwargs):
    payload = {
        "title": "Test Pasta",
        "ingredients": "pasta, tomato, garlic",
        "steps": "Boil pasta. Make sauce. Combine.",
        **kwargs,
    }
    return client.post("/recipes/", json=payload)


# ── Tests ──────────────────────────────────────────────────────────────────────
class TestRecipeEndpoints:
    def test_health(self):
        r = client.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_create_recipe_success(self):
        r = create_sample_recipe()
        assert r.status_code == 201
        data = r.json()
        assert data["title"] == "Test Pasta"
        assert data["dietary_focus"] in {"High Carb", "Balanced", "Low Calorie", "High Protein"}
        assert data["meal_type"] in {"Breakfast", "Lunch", "Dinner", "Snack"}

    def test_create_recipe_empty_title(self):
        r = client.post("/recipes/", json={"title": "", "ingredients": "egg", "steps": "Cook"})
        assert r.status_code == 422

    def test_create_recipe_invalid_meal_type(self):
        r = client.post("/recipes/", json={
            "title": "X", "ingredients": "egg", "steps": "Cook", "meal_type": "Brunch"
        })
        assert r.status_code == 422

    def test_list_recipes(self):
        create_sample_recipe(title="List Test")
        r = client.get("/recipes/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)
        assert len(r.json()) >= 1

    def test_get_recipe_by_id(self):
        r = create_sample_recipe(title="By ID")
        rid = r.json()["id"]
        r2 = client.get(f"/recipes/{rid}")
        assert r2.status_code == 200
        assert r2.json()["id"] == rid

    def test_get_recipe_not_found(self):
        r = client.get("/recipes/999999")
        assert r.status_code == 404

    def test_delete_recipe(self):
        r = create_sample_recipe(title="Delete Me")
        rid = r.json()["id"]
        d = client.delete(f"/recipes/{rid}")
        assert d.status_code == 204
        r2 = client.get(f"/recipes/{rid}")
        assert r2.status_code == 404

    def test_recommendations_match(self):
        create_sample_recipe(title="Tomato Pasta", ingredients="pasta, tomato, olive oil")
        r = client.get("/recommendations/?ingredients=pasta,tomato")
        assert r.status_code == 200
        data = r.json()
        assert len(data) >= 1
        assert data[0]["match_count"] >= 2

    def test_recommendations_no_match(self):
        r = client.get("/recommendations/?ingredients=durian,jackfruit")
        assert r.status_code == 200
        assert r.json() == []

    def test_recommendations_empty_ingredients(self):
        r = client.get("/recommendations/?ingredients=")
        assert r.status_code == 422

    def test_export_markdown(self):
        r = create_sample_recipe(title="Export Test")
        rid = r.json()["id"]
        e = client.get(f"/recipes/{rid}/export?format=markdown")
        assert e.status_code == 200
        assert "Export Test" in e.text

    def test_stats_endpoint(self):
        r = client.get("/stats/")
        assert r.status_code == 200
        assert "breakdown" in r.json()


class TestRecommendationLogic:
    def test_auto_tag_protein(self):
        from services.recommendation import auto_tag_dietary
        assert auto_tag_dietary("chicken, garlic, lemon") == "High Protein"

    def test_auto_tag_carb(self):
        from services.recommendation import auto_tag_dietary
        assert auto_tag_dietary("pasta, tomato, olive oil") == "High Carb"

    def test_auto_tag_balanced(self):
        from services.recommendation import auto_tag_dietary
        assert auto_tag_dietary("chicken, rice, broccoli") == "Balanced"

    def test_substitutions(self):
        from services.recommendation import get_substitutions
        subs = get_substitutions(["pine nuts", "butter"])
        assert subs["pine nuts"] == "walnuts"
        assert subs["butter"] == "olive oil"

    def test_substitution_missing_key(self):
        from services.recommendation import get_substitutions
        subs = get_substitutions(["dragon fruit"])
        assert subs == {}
