"""
Comprehensive test suite for the Mergington High School API.

Tests cover:
- GET /activities endpoint
- POST /activities/{activity_name}/signup endpoint
- DELETE /activities/{activity_name}/unregister endpoint
- GET / redirect functionality
"""

import pytest
from fastapi.testclient import TestClient


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns a 200 status code."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_all_activities(self, client):
        """Test that all 9 activities are returned."""
        response = client.get("/activities")
        data = response.json()
        assert len(data) == 9

    def test_get_activities_contains_chess_club(self, client):
        """Test that Chess Club is in the activities list."""
        response = client.get("/activities")
        data = response.json()
        assert "Chess Club" in data

    def test_activity_has_required_fields(self, client):
        """Test that each activity has the required fields."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_details in data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details

    def test_participants_is_list(self, client):
        """Test that participants field is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_details in data.values():
            assert isinstance(activity_details["participants"], list)

    def test_activity_has_initial_participants(self, client):
        """Test that activities have initial participants."""
        response = client.get("/activities")
        data = response.json()
        
        # Chess Club should have 2 initial participants
        assert len(data["Chess Club"]["participants"]) == 2


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_returns_200_on_success(self, client, test_email):
        """Test successful signup returns 200."""
        response = client.post(
            f"/activities/Chess%20Club/signup?email={test_email}"
        )
        assert response.status_code == 200

    def test_signup_returns_success_message(self, client, test_email):
        """Test successful signup returns success message."""
        response = client.post(
            f"/activities/Chess%20Club/signup?email={test_email}"
        )
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant_to_activity(self, client, test_email):
        """Test that signup adds participant to activity participants list."""
        # Get activities before signup
        response_before = client.get("/activities")
        participants_before = response_before.json()["Chess Club"]["participants"]
        
        # Sign up
        client.post(f"/activities/Chess%20Club/signup?email={test_email}")
        
        # Get activities after signup
        response_after = client.get("/activities")
        participants_after = response_after.json()["Chess Club"]["participants"]
        
        # Verify participant was added
        assert len(participants_after) == len(participants_before) + 1
        assert test_email in participants_after

    def test_signup_duplicate_returns_400(self, client, existing_participant):
        """Test signup returns 400 for duplicate email."""
        response = client.post(
            f"/activities/Chess%20Club/signup?email={existing_participant}"
        )
        assert response.status_code == 400

    def test_signup_duplicate_returns_error_detail(self, client, existing_participant):
        """Test duplicate signup returns error detail message."""
        response = client.post(
            f"/activities/Chess%20Club/signup?email={existing_participant}"
        )
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_invalid_activity_returns_404(self, client, test_email):
        """Test signup returns 404 for invalid activity."""
        response = client.post(
            f"/activities/InvalidActivity/signup?email={test_email}"
        )
        assert response.status_code == 404

    def test_signup_invalid_activity_returns_error_detail(self, client, test_email):
        """Test invalid activity signup returns error detail."""
        response = client.post(
            f"/activities/InvalidActivity/signup?email={test_email}"
        )
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_multiple_activities(self, client, test_email):
        """Test signup for multiple different activities."""
        # Sign up for Chess Club
        response1 = client.post(
            f"/activities/Chess%20Club/signup?email={test_email}"
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            f"/activities/Programming%20Class/signup?email={test_email}"
        )
        assert response2.status_code == 200
        
        # Verify in both activities
        response = client.get("/activities")
        data = response.json()
        assert test_email in data["Chess Club"]["participants"]
        assert test_email in data["Programming Class"]["participants"]


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_returns_200_on_success(self, client, existing_participant):
        """Test successful unregister returns 200."""
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={existing_participant}"
        )
        assert response.status_code == 200

    def test_unregister_returns_success_message(self, client, existing_participant):
        """Test successful unregister returns success message."""
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={existing_participant}"
        )
        data = response.json()
        assert "message" in data
        assert existing_participant in data["message"]

    def test_unregister_removes_participant(self, client, existing_participant):
        """Test that unregister removes participant from activity."""
        # Get participants before unregister
        response_before = client.get("/activities")
        participants_before = response_before.json()["Chess Club"]["participants"].copy()
        
        # Unregister
        client.delete(
            f"/activities/Chess%20Club/unregister?email={existing_participant}"
        )
        
        # Get participants after unregister
        response_after = client.get("/activities")
        participants_after = response_after.json()["Chess Club"]["participants"]
        
        # Verify participant was removed
        assert len(participants_after) == len(participants_before) - 1
        assert existing_participant not in participants_after

    def test_unregister_not_registered_returns_400(self, client, test_email):
        """Test unregister returns 400 if student not registered."""
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={test_email}"
        )
        assert response.status_code == 400

    def test_unregister_not_registered_returns_error_detail(self, client, test_email):
        """Test unregister error message for not registered student."""
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={test_email}"
        )
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_unregister_invalid_activity_returns_404(self, client, existing_participant):
        """Test unregister returns 404 for invalid activity."""
        response = client.delete(
            f"/activities/InvalidActivity/unregister?email={existing_participant}"
        )
        assert response.status_code == 404

    def test_unregister_invalid_activity_returns_error_detail(self, client, existing_participant):
        """Test unregister error message for invalid activity."""
        response = client.delete(
            f"/activities/InvalidActivity/unregister?email={existing_participant}"
        )
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unregister_then_signup_again(self, client, existing_participant):
        """Test that participant can sign up again after unregister."""
        # Unregister
        client.delete(
            f"/activities/Chess%20Club/unregister?email={existing_participant}"
        )
        
        # Sign up again
        response = client.post(
            f"/activities/Chess%20Club/signup?email={existing_participant}"
        )
        assert response.status_code == 200
        
        # Verify participant is back
        response = client.get("/activities")
        data = response.json()
        assert existing_participant in data["Chess Club"]["participants"]


class TestRootEndpoint:
    """Tests for GET / endpoint."""

    def test_root_returns_redirect(self, client):
        """Test that GET / returns a redirect status code."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307

    def test_root_redirects_to_static_html(self, client):
        """Test that GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert "/static/index.html" in response.headers.get("location", "")

    def test_root_redirect_destination_is_accessible(self, client):
        """Test that the redirect destination is accessible."""
        # Follow the redirect
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
