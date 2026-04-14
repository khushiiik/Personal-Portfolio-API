# REGISTRATION TEST.
def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "newuser",
            "email": "newuser@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "newuser"
    assert data["email"] == "newuser@test.com"
    assert "id" in data

    assert "password" not in data
    assert "hashed_password" not in data


# LOGIN TESTS
def test_login_success(client):
    client.post(
        "/auth/register",
        json={"name": "loginuser", "email": "login@test.com", "password": "mypassword"},
    )

    response = client.post(
        "/auth/login", data={"username": "login@test.com", "password": "mypassword"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
