from pydantic import BaseModel
from typing import List


class FoodItem(BaseModel):
    food_name: str
    quantity: int


class OrderRequest(BaseModel):
    employee_id: str
    employee_name: str
    items: List[FoodItem]



