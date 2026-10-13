import random
from unittest.mock import patch
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


def test_analytics_endpoints():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}


    product_response = client.post(
        "/products/",
        headers=headers,
        json={
            "name": f"Analytics Test Product {random.randint(1, 1000)}",
            "description": "Product for testing analytics",
            "price": 100.0,
            "stock": 50
        }
    )
    assert product_response.status_code in [200, 201]
    product_id = product_response.json()["id"]


    order_response = client.post(
        "/orders/",
        headers=headers,
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5
                }
            ]
        }
    )
    assert order_response.status_code in [200, 201]


    summary_response = client.get("/analytics/summary", headers=headers)
    assert summary_response.status_code == 200

    summary_data = summary_response.json()
    assert "total_orders" in summary_data
    assert "total_revenue" in summary_data


    assert summary_data["total_orders"] > 0
    assert summary_data["total_revenue"] >= 500.0


    top_products_response = client.get("/analytics/top-products", headers=headers)
    assert top_products_response.status_code == 200

    top_data = top_products_response.json()
    assert isinstance(top_data, list)
    assert len(top_data) > 0


    first_product = top_data[0]
    assert "product_name" in first_product
    assert "total_sold" in first_product
    assert "revenue" in first_product



@patch("app.api.assistant.Groq")
def test_ai_assistant_endpoint(mock_groq_class):
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}


    mock_instance = mock_groq_class.return_value
    mock_message = mock_instance.chat.completions.create.return_value.choices[0].message
    mock_message.content = "This is a mocked AI response based on your database analytics."


    response = client.post(
        "/ai/ask",
        headers=headers,
        json={
            "question": "What is our best selling product?"
        }
    )

    print("\n--- AI ASSISTANT MOCKED RESPONSE ---")
    print(response.json())
    print("------------------------------------\n")

    assert response.status_code == 200

    data = response.json()
    assert "answer" in data

    assert data["answer"] == "This is a mocked AI response based on your database analytics."