from fastapi import status

def test_create_invoice(client):
    # The endpoint maps input to model and returns it.
    invoice_data = {
        "id": 1,
        "customer": {
            "id": 1, 
            "name": "Inv Customer", 
            "email": "inv@test.com", 
            "age": 25,
            "description": "Test"
        },
        "transactions": [
             {
                 "id": 1,
                 "ammount": 100,
                 "description": "Item 1",
                 "customer_id": 1
             }
        ],
        "total": 100
    }
    
    response = client.post("/invoices", json=invoice_data)
    assert response.status_code == status.HTTP_200_OK
    
    # Check response (ignoring format differences like None vs missing if relevant)
    data = response.json()
    assert data["id"] == 1
    assert data["customer"]["email"] == "inv@test.com"
    assert data["total"] == 100
    assert len(data["transactions"]) == 1
