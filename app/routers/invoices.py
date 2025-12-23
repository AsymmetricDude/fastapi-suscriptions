from fastapi import APIRouter
from ..models import Invoice

router = APIRouter(tags=["invoices"])

@router.post("/invoices", response_model=Invoice)
async def create_invoice(invoice_data: Invoice):
    return invoice_data
