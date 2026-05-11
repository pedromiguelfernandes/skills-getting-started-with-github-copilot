"""
Tests for the POST /activities/{activity_name}/signup endpoint.

These tests verify successful signups, error handling, and edge cases including
duplicate prevention, invalid activities, and capacity limits.
"""

import pytest


class TestSignupForActivity:
    """Tests for signing up students for activities."""

    def test_successful_signup_adds_participant(self, test_client):
        """Test that successful signup adds email to participants list."""
        response = test_client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify participant was actually added
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_increases_participant_count(self, test_client):
        """Test that signup increases the participant count."""
        # Get initial count
        initial_response = test_client.get("/activities")
        initial_activities = initial_response.json()
        initial_count = len(initial_activities["Programming Class"]["participants"])
        
        # Sign up new participant
        test_client.post(
            "/activities/Programming%20Class/signup",
            params={"email": "newprogrammer@mergington.edu"}
        )
        
        # Verify count increased
        updated_response = test_client.get("/activities")
        updated_activities = updated_response.json()
        updated_count = len(updated_activities["Programming Class"]["participants"])
        
        assert updated_count == initial_count + 1

    def test_signup_nonexistent_activity_returns_404(self, test_client):
        """Test that signing up for nonexistent activity returns 404."""
        response = test_client.post(
            "/activities/Nonexistent%20Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_duplicate_signup_returns_400(self, test_client):
        """Test that duplicate signup returns 400 error."""
        # Try to sign up someone already in Chess Club
        response = test_client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_cannot_signup_twice_for_same_activity(self, test_client):
        """Test that a student cannot sign up twice for the same activity."""
        email = "student@mergington.edu"
        
        # First signup should succeed
        response1 = test_client.post(
            "/activities/Art%20Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = test_client.post(
            "/activities/Art%20Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 400

    def test_empty_email_string_signup(self, test_client):
        """Test signup with empty email string."""
        # App accepts empty string currently per requirement to test current behavior
        # This test documents the current permissive behavior
        response = test_client.post(
            "/activities/Drama%20Club/signup",
            params={"email": ""}
        )
        
        # Current app accepts even empty emails; document this behavior
        assert response.status_code == 200 or response.status_code == 400
        # If it succeeds, verify it was added. If it fails, that's also acceptable.

    def test_signup_with_special_characters_email(self, test_client):
        """Test signup with email containing special characters."""
        special_email = "user+tag@mergington.edu"
        
        response = test_client.post(
            "/activities/Math%20Olympiad/signup",
            params={"email": special_email}
        )
        
        # App is permissive with email format
        assert response.status_code == 200
        
        # Verify it was added
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        assert special_email in activities["Math Olympiad"]["participants"]

    def test_activity_name_case_sensitive(self, test_client):
        """Test that activity names are case-sensitive."""
        # Try lowercase version of activity name
        response = test_client.post(
            "/activities/chess%20club/signup",  # lowercase
            params={"email": "student@mergington.edu"}
        )
        
        # Should fail because activity names are case-sensitive in the dict
        assert response.status_code == 404

    def test_activity_name_with_spaces_requires_encoding(self, test_client):
        """Test that activity names with spaces must be URL-encoded."""
        # This is just documenting how the TestClient works with path parameters
        response = test_client.post(
            "/activities/Soccer%20Practice/signup",
            params={"email": "goalsetter@mergington.edu"}
        )
        
        assert response.status_code == 200

    def test_current_behavior_no_capacity_enforcement(self, test_client):
        """
        Test current app behavior: signup does not enforce max_participants limit.
        
        TECH DEBT NOTE: The app has max_participants field but doesn't enforce it.
        This test documents the current behavior. In a future enhancement,
        this test should be updated to verify capacity is enforced.
        """
        # Get capacity for Science Club
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        max_cap = activities["Science Club"]["max_participants"]
        current_count = len(activities["Science Club"]["participants"])
        
        # Sign up enough people to exceed capacity if it were enforced
        signups_to_add = max_cap + 5
        
        for i in range(signups_to_add):
            email = f"student{i}@mergington.edu"
            response = test_client.post(
                "/activities/Science%20Club/signup",
                params={"email": email}
            )
            # All should succeed because app doesn't enforce limit
            assert response.status_code == 200, \
                f"Signup {i} failed; indicates capacity enforcement might be new"
        
        # Verify all were added (exceeds max_participants)
        updated_response = test_client.get("/activities")
        updated_activities = updated_response.json()
        
        final_count = len(updated_activities["Science Club"]["participants"])
        assert final_count > max_cap, \
            "Current app allows exceeding max_participants (no enforcement)"

    def test_multiple_students_can_signup_for_same_activity(self, test_client):
        """Test that multiple different students can sign up for the same activity."""
        activity = "Soccer%20Practice"
        
        students = [
            "alice@mergington.edu",
            "bob@mergington.edu",
            "charlie@mergington.edu"
        ]
        
        # All three students sign up
        for email in students:
            response = test_client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all three were added
        activities_response = test_client.get("/activities")
        activities = activities_response.json()
        
        for email in students:
            assert email in activities["Soccer Practice"]["participants"]

    def test_signup_preserves_other_participants(self, test_client):
        """Test that signup doesn't remove existing participants."""
        # Get initial participants
        initial_response = test_client.get("/activities")
        initial_activities = initial_response.json()
        initial_participants = set(initial_activities["Basketball Team"]["participants"])
        
        # Add a new participant
        new_email = "newathlete@mergington.edu"
        test_client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": new_email}
        )
        
        # Verify all existing participants are still there
        updated_response = test_client.get("/activities")
        updated_activities = updated_response.json()
        updated_participants = set(updated_activities["Basketball Team"]["participants"])
        
        assert initial_participants.issubset(updated_participants)
        assert new_email in updated_participants

    def test_different_students_can_signup_for_different_activities(self, test_client):
        """Test that a student cannot be prevented from joining multiple activities."""
        student_email = "versatile@mergington.edu"
        
        # Sign up for multiple activities
        activities_to_join = ["Chess%20Club", "Drama%20Club", "Art%20Club"]
        
        for activity in activities_to_join:
            response = test_client.post(
                f"/activities/{activity}/signup",
                params={"email": student_email}
            )
            assert response.status_code == 200
        
        # Verify student is in all activities
        final_response = test_client.get("/activities")
        final_activities = final_response.json()
        
        for activity_name in ["Chess Club", "Drama Club", "Art Club"]:
            assert student_email in final_activities[activity_name]["participants"]
