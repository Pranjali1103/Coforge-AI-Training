from pydantic import BaseModel,Field 
from typing import Literal

class CustomerRequest(BaseModel):
    customer_id:str=Field(min_length=2)
    customer_name:str
    order_id:str=Field(min_length=2)
    rating:int=Field(ge=1,le=5)
    feedback:str=Field(min_length=10)

class CustomerResponse(BaseModel):
    customer_id:str
    sentiment:Literal["Positive","Neutral","Negative"]
    issue_category:Literal["Delivery","Product","Service","Other"]
    priority:Literal["High","Normal"]
    reply:str
    status:str

    


