import random
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


random_id = random.randint(10000, 99999)
TEST_USER_EMAIL = f"manager{random_id}@test.com"
TEST_USER_NAME = f"test_manager_{random_id}"
TEST_PASSWORD = "testpassword123"


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": TEST_USER_NAME,
            "email": TEST_USER_EMAIL,
            "password": TEST_PASSWORD,
            "role": "Manager"
        }
    )

    assert response.status_code in [200, 201]

    data = response.json()
    assert "id" in data
    assert data["email"] == TEST_USER_EMAIL
    assert data["role"] == "Manager"


def test_login_user():
    response = client.post(
        "/auth/login",
        data={
            "username": TEST_USER_EMAIL,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"