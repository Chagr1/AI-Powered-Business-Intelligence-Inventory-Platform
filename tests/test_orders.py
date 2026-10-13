import random
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_auth_token():
    random_id = random.randint(10000, 99999)
    email = f"admin{random_id}@test.com"
    password = "testpassword123"

    client.post(
        "/auth/register",
        json={"username": f"admin_{random_id}", "email": email, "password": password, "role": "admin"}
    )
    login_response = client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    return login_response.json()["access_token"]


def test_order_creates_and_reduces_stock():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. ADD NEW PRODUCT (STOCK: 10)
    product_response = client.post(
        "/products/",
        headers=headers,
        json={
            "name": "MacBook Pro M3",
            "description": "Test order product",
            "price": 2000.0,
            "stock": 10
        }
    )
    assert product_response.status_code in [200, 201]
    product_id = product_response.json()["id"]

    # 2. PLACE ORDER (QUANTITY: 2)
    order_response = client.post(
        "/orders/",
        headers=headers,
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2
                }
            ]
        }
    )
    assert order_response.status_code in [200, 201]

    # 3. VERIFY STOCK REDUCTION
    # Fetch all products to find our updated product
    check_products_response = client.get("/products/", headers=headers)
    assert check_products_response.status_code == 200

    all_products = check_products_response.json()

    updated_product = None
    for p in all_products:
        if p["id"] == product_id:
            updated_product = p
            break

    assert updated_product is not None, "Added product not found in the list!"

    print("\n--- STOCK CHECK ---")
    print(f"Initial: 10 | Sold: 2 | Remaining: {updated_product['stock']}")
    print("-------------------\n")

    # Assert that stock has been reduced by exactly 2
    assert updated_product["stock"] == 8