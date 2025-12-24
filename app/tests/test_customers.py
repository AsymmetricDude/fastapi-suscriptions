from fastapi import status

def test_create_customer(client):
    response = client.post(
        "/customers",
        json={"name": "John Doe", "email": "john.doe@example.com", "age": 30}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["age"] == 30
    assert data["id"] is not None

def test_create_customer_duplicate_email(client):
    # Create first customer
    client.post(
        "/customers",
        json={"name": "Double", "email": "double@example.com", "age": 30}
    )
    # Try to create second with same email
    response = client.post(
        "/customers",
        json={"name": "Double 2", "email": "double@example.com", "age": 25}
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Customer with this email already exists"

def test_read_customer(client):
    # Create a customer first
    response_create = client.post(
        "/customers",
        json={"name": "Alice", "email": "alice@example.com", "age": 28}
    )
    customer_id = response_create.json()["id"]

    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["age"] == 28
    assert data["id"] == customer_id

def test_read_customer_not_found(client):
    response = client.get("/customers/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_customer(client):
    # Create customer
    response_create = client.post(
        "/customers",
        json={"name": "Bob", "email": "bob@example.com", "age": 40}
    )
    customer_id = response_create.json()["id"]

    # Update customer
    response = client.patch(
        f"/customers/{customer_id}",
        json={"name": "Bob Updated", "age": 41}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Bob Updated"
    assert data["age"] == 41
    assert data["email"] == "bob@example.com" # Should remain unchanged

def test_delete_customer(client):
    # Create customer
    response_create = client.post(
        "/customers",
        json={"name": "Charlie", "email": "charlie@example.com", "age": 35}
    )
    customer_id = response_create.json()["id"]

    # Delete customer
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == status.HTTP_200_OK

    # Verify deleted
    response_get = client.get(f"/customers/{customer_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND

def test_list_customers(client):
    # Create a few customers
    client.post("/customers", json={"name": "List One", "email": "list1@example.com", "age": 20})
    client.post("/customers", json={"name": "List Two", "email": "list2@example.com", "age": 22})

    response = client.get("/customers")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    # Check if the created customers are in the list
    emails = [c["email"] for c in data]
    assert "list1@example.com" in emails
    assert "list2@example.com" in emails
