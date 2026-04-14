def test_create_project(client, auth_headers):

    response = client.post(
        "/project/",
        json={
            "title": "Portfolio API",
            "project_link": "https://github.com/test/portfolio-api",
            "description": "A FastAPI project for managing portfolio data",
            "is_current": False,
            "start_date": "2025-01-01",
            "end_date": "2025-03-01",
            "skills": [{"name": "FastAPI"}, {"name": "SQLAlchemy"}],
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Portfolio API"
    assert data["is_current"] == False
    assert data["start_date"] == "2025-01-01"
    assert "id" in data


def test_create_project_no_token(client):
    response = client.post(
        "/project/",
        json={
            "title": "Portfolio API",
            "project_link": "https://github.com/test/portfolio-api",
            "description": "A FastAPI project for managing portfolio data",
            "is_current": False,
            "start_date": "2025-01-01",
            "end_date": "2025-03-01",
            "skills": [{"name": "FastAPI"}, {"name": "SQLAlchemy"}],
        },
    )

    assert response.status_code == 401
