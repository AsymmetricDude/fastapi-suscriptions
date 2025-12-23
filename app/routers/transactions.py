from fastapi import APIRouter, HTTPException, status
from ..models import Transaction, TransactionCreate
from ..db import SessionDep
from sqlmodel import select
from ..models.customers import Customer


router = APIRouter(tags=["transactions"])

@router.post("/transactions")
async def create_transation(transaction_data: TransactionCreate, session: SessionDep, status_code=status.HTTP_201_CREATED):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    transaction = Transaction.model_validate(transaction_data_dict)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.get("/transactions")
async def list_transaction(session: SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions
