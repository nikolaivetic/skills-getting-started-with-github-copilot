"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_get_activities_returns_all_activities(client):
    """Test: GET /activities returns all activities"""
    # Arrange: (data already set up via fixtures)

    # Act: Request all activities
    response = client.get("/activities")

    # Assert: Verify response and content
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_has_correct_structure(client):
    """Test: Activity response has all required fields"""
    # Arrange: (data ready)

    # Act: Get activities
    response = client.get("/activities")
    data = response.json()

    # Assert: Check structure
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participant_count(client):
    """Test: Participant counts are accurate"""
    # Arrange: (data ready)

    # Act: Get activities
    response = client.get("/activities")
    data = response.json()

    # Assert: Verify participant counts match
    assert len(data["Chess Club"]["participants"]) == 1
    assert len(data["Programming Class"]["participants"]) == 1
