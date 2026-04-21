from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.database import Base, engine
from routers import recipes, websocket

# Create tables (also handled by Alembic, but useful for dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recipe Sharing & Recommendation API",
    description=(
        "A full-stack recipe platform with rule-based recommendations, "
        "nutritional auto-tagging, time-based suggestions, smart substitutions, "
        "real-time WebSocket broadcasts, and export (Markdown/PDF)."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes.router)
app.include_router(websocket.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Recipe API is running 🍳"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
