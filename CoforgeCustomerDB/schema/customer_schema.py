from decimal import Decimal
from pydantic import(
    BaseModel,Field,EmailStr,ConfigDict
)
class CustomerBase(BaseModel):
    customer_name:str=Field(min_length=2)
    age:int=Field(ge=18,le=70)
    email:EmailStr
    department:str=Field(min_length=2)
    designation:str=Field(min_length=2)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id:int
    model_config=ConfigDict(from_attributes=True)

