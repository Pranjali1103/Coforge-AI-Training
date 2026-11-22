from pydantic import EmailStr,BaseModel,Field,ConfigDict
from typing import Literal
from decimal import Decimal
from datetime import date

class BankCustomerBase(BaseModel):
    customer_name: str = Field(min_length=2)
    email: EmailStr
    account_number: str = Field(min_length=3)
    account_type: Literal["Savings", "Current"]
    branch_name: str = Field(min_length=2)
    balance: Decimal = Field(ge=0)
    is_active: bool
    opened_on: date


class BankCustomerCreate(BankCustomerBase):
    pass

class BankCustomerUpdate(BaseModel):
    customer_name: str = Field(min_length=2)
    email: EmailStr
    branch_name: str = Field(min_length=2)


class BankCustomerResponse(BankCustomerBase):
    customer_id: int
    model_config = ConfigDict(from_attributes=True)

class AmountUpdate(BaseModel):
    amount: Decimal = Field(gt=0)

