"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_successful_signup(client):
    """Test: Successfully sign up a new student"""
    # Arrange: Prepare email and activity
    email = "alice@mergington.edu"
    activity = "Chess Club"

    # Act: Post signup request
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify success and participant added
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_duplicate_signup_rejected(client):
    """Test: Reject duplicate signup"""
    # Arrange: Register a student first
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act: Attempt duplicate signup
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify rejection
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test: Reject signup for non-existent activity"""
    # Arrange: Prepare invalid activity name
    email = "alice@mergington.edu"
    activity = "Nonexistent Club"

    # Act: Post signup request
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify not found
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_increments_participant_count(client):
    """Test: Signing up increments participant count from API"""
    # Arrange: Get initial participant count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()["Chess Club"]["participants"])
    email = "bob@mergington.edu"

    # Act: Sign up new student
    client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert: Verify count increased by 1
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()["Chess Club"]["participants"])
    assert updated_count == initial_count + 1
