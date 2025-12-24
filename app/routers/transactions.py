from fastapi import APIRouter, HTTPException, status, Query
from ..models import Transaction, TransactionCreate
from ..db import SessionDep
from sqlmodel import select, func
from ..models.customers import Customer



router = APIRouter(tags=["transactions"])

@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transation(transaction_data: TransactionCreate, session: SessionDep):
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
async def list_transaction(session: SessionDep, offset: int = Query(default=0, description="Number of transactions to skip"), limit: int = Query(default=10, description="Number of transactions to return")):
    query = select(Transaction).offset(offset).limit(limit)
    transactions = session.exec(query).all()
    return {
        "transactions": transactions,
        "offset": offset,
        "limit": limit,
        "total": session.scalar(select(func.count()).select_from(Transaction))
    }
