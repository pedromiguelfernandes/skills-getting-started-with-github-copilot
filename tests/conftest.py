"""
Pytest configuration and shared fixtures for FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_client():
    """Provides a TestClient for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Provides a copy of the sample activities data.
    
    This fixture returns a fresh copy of the activities structure for each test,
    preventing test pollution. The activities dict has initial participants
    that should be reset after each test.
    """
    return {
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
            "description": "Practice skills and play competitive basketball games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
        },
        "Soccer Practice": {
            "description": "Develop teamwork and soccer techniques on the field",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["nina@mergington.edu", "leo@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["clara@mergington.edu", "maria@mergington.edu"]
        },
        "Drama Club": {
            "description": "Rehearse plays, practice acting, and perform for the school",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["julia@mergington.edu", "sam@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific ideas together",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
        }
    }


@pytest.fixture(autouse=True)
def reset_activities(sample_activities):
    """
    Auto-use fixture that resets the global activities dict before each test.
    
    This prevents test pollution by ensuring each test starts with fresh,
    consistent state. The fixture runs automatically before every test.
    """
    # Clear and repopulate activities with fresh data
    activities.clear()
    activities.update(sample_activities)
    
    yield  # Run the test
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(sample_activities)
