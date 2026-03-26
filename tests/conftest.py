"""
Pytest configuration and shared fixtures for FastAPI app tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities for resetting between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Compete in basketball games and tournaments",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and play matches",
        "schedule": "Thursdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["sarah@mergington.edu", "alex@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["jessica@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Play instruments and perform in concerts",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["ryan@mergington.edu", "maya@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["natalie@mergington.edu", "david@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Provides a TestClient for making requests to the FastAPI app.
    Resets the activities data before each test to ensure test isolation.
    """
    # Reset activities to original state
    activities.clear()
    activities.update({
        name: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy()
        }
        for name, details in ORIGINAL_ACTIVITIES.items()
    })
    
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """
    Provides sample activity data for testing.
    """
    return {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    }


@pytest.fixture
def test_email():
    """
    Provides a test email for signup/unregister operations.
    """
    return "test.student@mergington.edu"


@pytest.fixture
def existing_participant():
    """
    Provides an existing participant email from the activities.
    """
    return "michael@mergington.edu"
