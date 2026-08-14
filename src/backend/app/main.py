from fastapi import FastAPI

app = FastAPI(title="SignalShop API")

@app.get("/health")
def health():
    return {"status": "ok"}