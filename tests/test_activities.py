"""
Tests for the GET /activities endpoint.

These tests verify that the activities list is returned correctly with all expected
activities and their data structure.
"""

import pytest


class TestGetActivities:
    """Tests for retrieving the list of all activities."""

    def test_get_activities_returns_all_activities(self, test_client):
        """Test that /activities returns all 9 activities."""
        response = test_client.get("/activities")
        
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
        assert "Basketball Team" in activities
        assert "Soccer Practice" in activities
        assert "Art Club" in activities
        assert "Drama Club" in activities
        assert "Math Olympiad" in activities
        assert "Science Club" in activities

    def test_activity_structure_contains_required_fields(self, test_client):
        """Test that each activity has all required fields."""
        response = test_client.get("/activities")
        activities = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
            assert required_fields.issubset(activity_data.keys()), \
                f"{activity_name} missing required fields"

    def test_activity_participants_is_list(self, test_client):
        """Test that participants field is a list for each activity."""
        response = test_client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants should be a list"

    def test_activity_max_participants_is_numeric(self, test_client):
        """Test that max_participants field is numeric for each activity."""
        response = test_client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} max_participants should be an integer"
            assert activity_data["max_participants"] > 0, \
                f"{activity_name} max_participants should be positive"

    def test_chess_club_has_initial_participants(self, test_client):
        """Test that Chess Club has initial participants."""
        response = test_client.get("/activities")
        activities = response.json()
        
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]

    def test_programming_class_has_correct_description(self, test_client):
        """Test Programming Class has expected description."""
        response = test_client.get("/activities")
        activities = response.json()
        
        prog_class = activities["Programming Class"]
        expected_desc = "Learn programming fundamentals and build software projects"
        assert prog_class["description"] == expected_desc

    def test_response_is_dict_not_list(self, test_client):
        """Test that response is a dict/object, not a list."""
        response = test_client.get("/activities")
        data = response.json()
        
        assert isinstance(data, dict), "Response should be a dictionary of activities"

    def test_all_activities_have_descriptions(self, test_client):
        """Test that all activities have non-empty descriptions."""
        response = test_client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert activity_data.get("description"), \
                f"{activity_name} should have a description"
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0

    def test_all_activities_have_schedules(self, test_client):
        """Test that all activities have non-empty schedules."""
        response = test_client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert activity_data.get("schedule"), \
                f"{activity_name} should have a schedule"
            assert isinstance(activity_data["schedule"], str)
            assert len(activity_data["schedule"]) > 0
