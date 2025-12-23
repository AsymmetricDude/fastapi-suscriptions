from sqlmodel import SQLModel, Field, Relationship

class TransactionBase(SQLModel):
    ammount: int
    description: str

class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id") 
    customer: "Customer" = Relationship(back_populates="transactions")
    
class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id") 