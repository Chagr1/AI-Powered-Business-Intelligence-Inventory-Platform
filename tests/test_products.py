import random
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_auth_token():
    random_id = random.randint(10000, 99999)
    email = f"admin{random_id}@test.com"
    password = "testpassword123"


    reg_response = client.post(
        "/auth/register",
        json={
            "username": f"admin_{random_id}",
            "email": email,
            "password": password,
            "role": "admin"
        }
    )


    print("\n--- REGISTRATION RESULT ---")
    print(reg_response.json())
    print("---------------------------\n")

    login_response = client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    return login_response.json()["access_token"]


def test_create_product():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/products",
        headers=headers,
        json={
            "name": "Test Laptop",
            "description": "High performance test laptop",
            "price": 1500.0,
            "stock": 50,
            "category": "Electronics"
        }
    )

    print("\n--- CREATE PRODUCT DETAILS ---")
    print(response.json())
    print("------------------------------\n")

    assert response.status_code in [200, 201]