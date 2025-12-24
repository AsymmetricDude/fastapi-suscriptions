from fastapi import status

def test_create_plan(client):
    response = client.post(
        "/plans",
        json={"name": "Basic Plan", "price": 100, "description": "Basic description"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Basic Plan"
    assert data["price"] == 100
    assert data["id"] is not None

def test_list_plans(client):
    # Create two plans
    client.post("/plans", json={"name": "Plan A", "price": 10, "description": "A"})
    client.post("/plans", json={"name": "Plan B", "price": 20, "description": "B"})

    response = client.get("/plans")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    # Ensure at least 2 are there
    assert len(data) >= 2
