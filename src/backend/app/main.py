from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, catalog, cart, orders, customers, signal, scheduling, delivery, conversations, users, notifications, settings, ratings, permissions, statistics, export, audit

app = FastAPI(title="SignalShop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(catalog.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(signal.router, prefix="/api/v1")
app.include_router(scheduling.router, prefix="/api/v1")
app.include_router(delivery.router, prefix="/api/v1")
app.include_router(conversations.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(settings.router, prefix="/api/v1")
app.include_router(ratings.router, prefix="/api/v1")
app.include_router(permissions.router, prefix="/api/v1")
app.include_router(statistics.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")
app.include_router(audit.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}