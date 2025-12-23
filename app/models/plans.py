from sqlmodel import SQLModel, Field, Relationship
from typing import List
from .customers import Customer
from .customer_plans import CustomerPlan, StatusEnum

class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)        
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: List[Customer] = Relationship(back_populates="plans", link_model=CustomerPlan)