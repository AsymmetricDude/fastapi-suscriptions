from fastapi import APIRouter, status
from ..models import Plan
from ..db import SessionDep
from sqlmodel import select
from ..models.plans import Plan
from ..models.customer_plans import CustomerPlan


router = APIRouter(tags=["plans"])

@router.post("/plans")
def create_plan(plan_data: Plan, session: SessionDep, status_code=status.HTTP_201_CREATED):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@router.get("/plans", response_model=list[Plan])
def get_plans(session: SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans

