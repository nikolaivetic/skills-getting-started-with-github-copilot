import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def mock_activities():
    """Arrange: Provide clean mock activity data for each test"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        }
    }


@pytest.fixture
def client(mock_activities, monkeypatch):
    """Arrange: Set up test client with isolated mock data"""
    monkeypatch.setattr("src.app.activities", mock_activities)
    return TestClient(app)
