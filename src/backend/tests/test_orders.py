from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order_requires_cart():
    response = client.post("/api/v1/orders", json={"cart_id": None})
    assert response.status_code == 400