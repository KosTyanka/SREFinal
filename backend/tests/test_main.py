from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Concert Ticketing API"}

def test_get_concerts():
    response = client.get("/concerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"} 