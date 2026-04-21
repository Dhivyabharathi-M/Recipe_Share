# 🍳 RecipeShare – Recipe Sharing & Recommendation App

A full-stack recipe platform built with **FastAPI** (backend), **ReactJS** (frontend), **SQLite + SQLAlchemy + Alembic** (database), with rule-based recommendations, real-time WebSocket notifications, export features, and auto-generated Python SDK.

---

## 📁 Project Structure

```
recipe-app/
├── backend/
│   ├── main.py                        # FastAPI app entry point
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/
│   │       └── 0001_initial.py        # Initial migration
│   ├── models/
│   │   └── database.py                # SQLAlchemy models + DB session
│   ├── schemas/
│   │   └── recipe.py                  # Pydantic request/response models
│   ├── routers/
│   │   ├── recipes.py                 # All REST endpoints
│   │   └── websocket.py               # WebSocket endpoint
│   ├── services/
│   │   ├── recommendation.py          # Core recommendation engine
│   │   ├── export.py                  # Markdown + PDF export
│   │   └── websocket_manager.py       # WS connection manager
│   └── tests/
│       └── test_recipes.py            # Unit tests (pytest)
├── frontend/
│   ├── package.json
│   ├── public/index.html
│   └── src/
│       ├── App.js                     # Root component + tab nav
│       ├── App.css                    # Full design system
│       ├── index.js
│       ├── components
│       ├── hooks/
│       │   └── useWebSocket.js        # Auto-reconnecting WS hook
│       └── services/
│           └── api.js                 # Axios API layer
├── seed/
│   └── seed_data.sql                  # 10 sample recipes
├── scripts/
│   ├── generate_sdk.sh
│   └── generate_sdk.bat
├── setupdev.bat                       # Windows setup script
├── setupdev.sh                        # macOS/Linux setup script
├── runapplication.bat                 # Windows run script
└── runapplication.sh                  # macOS/Linux run script
```

---

## ⚙️ Setup & Installation

### Prerequisites
| Tool | Minimum Version |
|------|----------------|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |

### Windows
```bat
setupdev.bat
```

### macOS / Linux
```bash
chmod +x setupdev.sh runapplication.sh scripts/generate_sdk.sh
./setupdev.sh
```

---

## 🚀 Running the Application

### Windows
```bat
runapplication.bat
```

### macOS / Linux
```bash
./runapplication.sh
```

| Service | URL |
|---------|-----|
| FastAPI Backend | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| React Frontend | http://localhost:3000 |

---

## 🔌 API Endpoints

### Recipes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/recipes/` | Add a new recipe |
| GET | `/recipes/` | List all recipes (filterable by `meal_type`) |
| GET | `/recipes/{id}` | Get single recipe |
| DELETE | `/recipes/{id}` | Delete recipe |
| GET | `/recipes/{id}/export?format=markdown` | Export as Markdown |
| GET | `/recipes/{id}/export?format=pdf` | Export as PDF |

### Recommendations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommendations/?ingredients=tomato,pasta` | Rule-based recommendations |
| GET | `/recommendations/?ingredients=egg&time_based=true` | Time-filtered recs |

### Stats & WebSocket
| | Endpoint | Description |
|-|----------|-------------|
| GET | `/stats/` | Dietary + meal type breakdown (for charts) |
| WS | `/ws` | Real-time recipe broadcast |

---

## 🧠 Core Features Explained

### 1. Rule-Based Recommendation Engine
```
Input:  ["tomato", "pasta"]
Logic:  For each stored recipe, count matching ingredients
        Sort by match count descending
        Return top-K results with match score %
Output: Ranked list of recipes with match percentage
```

### 2. Nutritional Auto-Tagging
Recipes are automatically classified on creation:
- **High Protein** → contains: chicken, egg, tofu, lentils, beef, fish…
- **High Carb** → contains: rice, pasta, bread, potato, oats…
- **Balanced** → contains both protein and carb sources
- **Low Calorie** → neither protein nor carb keywords found

### 3. Time-Based Meal Suggestions
| Time | Meal Type |
|------|-----------|
| 05:00–10:59 | Breakfast 🌅 |
| 11:00–15:59 | Lunch ☀️ |
| 16:00–20:59 | Dinner 🌙 |
| 21:00–04:59 | Snack 🍎 |

Recommendations can optionally be filtered by current time of day.

### 4. Smart Substitution Logic
When an ingredient is missing, the engine suggests alternatives:
```
Missing: pine nuts    → Use: walnuts
Missing: butter       → Use: olive oil
Missing: cream        → Use: coconut cream
Missing: sour cream   → Use: Greek yogurt
```

### 5. Real-Time WebSocket Notifications
- Frontend connects to `ws://localhost:8000/ws` on load
- When any user adds a recipe via `POST /recipes/`, the backend broadcasts:
  ```json
  { "event": "new_recipe", "id": 5, "title": "Pesto Pasta", "message": "New recipe added: Pesto Pasta" }
  ```
- Frontend displays a toast notification and auto-refreshes the recipe list

### 6. Export Feature
- **Markdown** – clean `.md` file with title, metadata, ingredient list, and steps
- **PDF** – formatted PDF generated server-side using `reportlab`

---

## 🧪 Running Tests

```bash
cd backend
source env/bin/activate   # Windows: env\Scripts\activate
pytest tests/ -v
```

Tests cover:
- CRUD endpoints (create, list, get, delete)
- Input validation (empty title, invalid meal type)
- Recommendation matching and zero-match cases
- Markdown export
- Auto-tagging logic
- Substitution dictionary

---

## 🛠️ SDK Generation

### Step 1 – Ensure backend is running
```bash
./runapplication.sh   # or runapplication.bat on Windows
```

### Step 2 – Generate the SDK
```bash
# macOS/Linux
./scripts/generate_sdk.sh

# Windows
scripts\generate_sdk.bat
```

### Step 3 – Install the SDK
```bash
cd recipe_sdk
pip install -e .
```

### Step 4 – Use the SDK
```python
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
result = api.create_recipe_recipes_post(RecipeCreate(
    title="Garlic Bread",
    ingredients="bread, garlic, butter, parsley",
    steps="Mix garlic and butter, spread on bread, bake 10 min at 180°C"
))
print("Created:", result.id, result.title)

# Get recommendations
from recipe_sdk.api.recommendations_api import RecommendationsApi
rec_api = RecommendationsApi(client)
recs = rec_api.get_recommendations_recommendations_get(ingredients="bread,garlic")
for r in recs:
    print(r.recipe.title, f"- {r.match_score}% match")
```

---

## 🎨 Frontend Features

| Feature | Description |
|---------|-------------|
| Dynamic greeting | "Good Morning! Let's find breakfast 🌅" based on time |
| Chip/tag ingredient input | Press Enter or comma to add tags |
| Smart badges | High Protein 🔴, High Carb 🟡, Balanced 🟢, Low Calorie 🔵 |
| Meal type filter | Filter recipe list by Breakfast/Lunch/Dinner/Snack |
| Match score bar | Visual % bar showing ingredient match strength |
| Substitution hints | "💡 Missing pine nuts → Use walnuts instead" |
| Export buttons | Download `.md` or `.pdf` directly from any recipe card |
| Real-time toast | WebSocket-powered notification on new recipe creation |
| Charts | Pie (dietary breakdown) + Bar (meal type counts) via Recharts |

---

## 📦 Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI 0.111 |
| Database ORM | SQLAlchemy 2.0 |
| Migrations | Alembic 1.13 |
| Database | SQLite |
| Validation | Pydantic v2 |
| PDF export | ReportLab |
| Real-time | FastAPI WebSockets |
| Frontend | React 18 |
| HTTP client | Axios |
| Charts | Recharts |
| Notifications | react-hot-toast |
| SDK | OpenAPI Generator CLI |
| Tests | pytest + FastAPI TestClient |
