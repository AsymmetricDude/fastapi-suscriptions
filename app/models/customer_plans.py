from sqlmodel import SQLModel, Field
from enum import Enum
        
class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class CustomerPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    state: StatusEnum = Field(default=StatusEnum.ACTIVE)