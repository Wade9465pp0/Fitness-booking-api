from fastapi.testclient import TestClient
from app.main import app
import os
from app.database import init_db

client = TestClient(app)

def setup_module(module):
    # Recreate a clean database before running tests
    if os.path.exists("studio.db"):
        os.remove("studio.db")
    init_db()
    
def test_get_classes():
    response = client.get("/classes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_booking_success():
    response = client.post("/book", json={
        "class_id": 1,
        "client_name": "Test User",
        "client_email": "test@example.com"
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_booking_failure_overbook():
    # Intentionally book a class until it runs out (assuming 1 slot in seed)
    for _ in range(6):  # assuming seed has 5 slots
        client.post("/book", json={
            "class_id": 1,
            "client_name": "Spammer",
            "client_email": "spam@example.com"
        })
    # This one should fail
    response = client.post("/book", json={
        "class_id": 1,
        "client_name": "Late Comer",
        "client_email": "late@example.com"
    })
    assert response.status_code == 400
    assert "No slots available" in response.text
