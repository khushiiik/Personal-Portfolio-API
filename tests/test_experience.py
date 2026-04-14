def test_create_experience(client, auth_headers):

    response = client.post(
        "/experience/",
        json={
            "role": "test-role",
            "company": "test-company",
            "description": "test-description",
            "start_date": "2026-01-01",
            "end_date": "2026-02-01",
            "is_current": False,
            "skills": [{"name": "test-skill-1"}, {"name": "test-skill-2"}],
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()

    assert data["role"] == "test-role"
    assert data["is_current"] == False
    assert data["start_date"] == "2026-01-01"
    assert "id" in data


def test_create_experience_no_token(client):
    response = client.post(
        "/experience/",
        json={
            "role": "test-role",
            "company": "test-company",
            "description": "test-description",
            "start_date": "2026-01-01",
            "end_date": "2026-02-01",
            "is_current": False,
            "skills": [{"name": "test-skill-1"}, {"name": "test-skill-2"}],
        },
    )

    assert response.status_code == 401
