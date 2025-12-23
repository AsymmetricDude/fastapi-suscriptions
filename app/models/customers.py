from sqlmodel import SQLModel, Field, Relationship
from typing import List
from pydantic.networks import EmailStr
from .customer_plans import CustomerPlan
from pydantic import field_validator

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None, unique=True)
    age: int = Field(default=None)

    @field_validator("age")
    def validate_age(cls, v):
        if v < 18:
            raise ValueError("Invalid age")
        return v
        

class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list["Plan"] = Relationship(back_populates="customers", link_model=CustomerPlan)
