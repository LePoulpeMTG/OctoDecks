from fastapi import FastAPI
from routers import cards, sets

app = FastAPI(title="OctoDecks API")

# Route de test
@app.get("/")
def home():
    return {"msg": "Bienvenue sur l'API OctoDecks 🐙"}

# Routes principales
app.include_router(cards.router, prefix="/cards", tags=["Cards"])
app.include_router(sets.router, prefix="/sets", tags=["Sets"])
