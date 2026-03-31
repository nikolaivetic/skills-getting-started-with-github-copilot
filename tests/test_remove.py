"""Tests for DELETE /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_successful_removal(client):
    """Test: Successfully remove a student"""
    # Arrange: Prepare participant to remove
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act: Delete signup
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify removal and no longer in list
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_remove_nonexistent_student(client):
    """Test: Reject removal of student not signed up"""
    # Arrange: Prepare non-registered student
    email = "alice@mergington.edu"
    activity = "Chess Club"

    # Act: Delete signup
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify not found error
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_remove_from_nonexistent_activity(client):
    """Test: Reject removal from non-existent activity"""
    # Arrange: Prepare invalid activity
    email = "michael@mergington.edu"
    activity = "Nonexistent Club"

    # Act: Delete signup
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert: Verify not found
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_decrements_participant_count(client):
    """Test: Removing student decrements participant count"""
    # Arrange: Get initial participant count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()["Chess Club"]["participants"])
    email = "michael@mergington.edu"

    # Act: Remove student
    client.delete(f"/activities/Chess Club/signup?email={email}")

    # Assert: Verify count decreased by 1
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()["Chess Club"]["participants"])
    assert updated_count == initial_count - 1
