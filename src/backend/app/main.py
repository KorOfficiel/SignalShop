from fastapi import FastAPI
from app.api import auth

app = FastAPI(title="SignalShop API")

# Inclure les routes d'authentification
app.include_router(auth.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}