from fastapi import status

def test_create_transaction(client):
    # Need a customer first
    customer_res = client.post(
        "/customers",
        json={"name": "Transactor", "email": "trans@test.com", "age": 30}
    )
    customer_id = customer_res.json()["id"]

    response = client.post(
        "/transactions",
        json={"ammount": 500, "description": "Test Trans", "customer_id": customer_id}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["ammount"] == 500
    assert data["customer_id"] == customer_id
    assert data["id"] is not None

def test_create_transaction_invalid_customer(client):
    response = client.post(
        "/transactions",
        json={"ammount": 500, "description": "Test Trans", "customer_id": 99999}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_transactions(client):
    # Create customer and transaction
    customer_res = client.post(
        "/customers",
        json={"name": "Lister", "email": "list@test.com", "age": 30}
    )
    c_id = customer_res.json()["id"]
    client.post("/transactions", json={"ammount": 10, "description": "T1", "customer_id": c_id})
    
    response = client.get("/transactions")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Expecting: {"transactions": [...], "offset": 0, "limit": 10, "total": ...}
    assert "transactions" in data
    assert "total" in data
    assert len(data["transactions"]) >= 1
