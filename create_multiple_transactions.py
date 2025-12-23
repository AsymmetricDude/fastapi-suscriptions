from sqlmodel import Session

from app.db import engine
from app.models import Customer, Transaction

session = Session(engine)
customer = Customer(
    name="Julian",
    description="Estudiante",
    email="hola@lcmartinez.com",
    age=25,
)
session.add(customer)
session.commit()

for x in range(100):
    session.add(
        Transaction(
            customer_id=customer.id,
            description=f"Test number {x}",
            ammount=10 * x,
        )
    )
session.commit()