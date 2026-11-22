from decimal import Decimal
from pydantic import BaseModel,Field,ConfigDict

class EmployeePerformanceBase(BaseModel):
    employee_name:str=Field(min_length=2)
    department:str=Field(min_length=2)
    designation:str=Field(min_length=2)
    salary:Decimal=Field(gt=0)
    performance_rating:float=Field(ge=1,le=5)
    projects_completed:int=Field(ge=0)
    attendance_percentage:float=Field(ge=0,le=100)
    review_year:int 

class EmployeePerformanceCreate(EmployeePerformanceBase):
    pass

class EmployeePerformanceUpdate(BaseModel):
    performance_rating:float=Field(ge=1 ,le=5)
    projects_completed:int=Field(ge=0)
    attendance_percentage:float=Field(ge=0,le=100)

class EmployeePerformanceResponse(EmployeePerformanceBase):
    employee_id:int
    model_config=ConfigDict(from_attributes=True)

