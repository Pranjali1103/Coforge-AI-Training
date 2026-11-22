from fastapi import FastAPI
# from sqlalchemy.orm import Session
from config.database import Base,engine,SessionLocal
from schemas.employeeperformance_schema import EmployeePerformanceCreate,EmployeePerformanceResponse,EmployeePerformanceUpdate
from services import employeeperformance_service as service

app=FastAPI(title="Employee Performance Management API ")

Base.metadata.create_all(bind=engine)

@app.post("/employeesCreate",response_model=EmployeePerformanceResponse,status_code=201)
def create_employee(employee:EmployeePerformanceCreate):
    db=SessionLocal()
    try:
        return service.create_employee(db,employee)
    finally:
        db.close()


@app.get("/employeesGetAll",response_model=list[EmployeePerformanceResponse])
def get_all_employees(skip:int=0,limit:int=10):
    db=SessionLocal()
    try:
        return service.get_all_employees(db,skip,limit)
    finally:
        db.close()



@app.get("/employeesGetEmployeeById/{employee_id}",response_model=EmployeePerformanceResponse)
def get_employee_by_id(employee_id:int):
    db=SessionLocal()
    try:
        return service.get_employee_by_id(db,employee_id)
    finally:
        db.close()



@app.put("/employeeUpdate/{employee_id}",response_model=EmployeePerformanceResponse)
def update_employee(employee_id:int,data:EmployeePerformanceUpdate):
    db=SessionLocal()
    try:
        return service.update_employee(db,employee_id,data)
    finally:
        db.close()



@app.get("/employeesByDepartment/{dept}",response_model=list[EmployeePerformanceResponse])
def get_employee_by_dept(dept:str):
    db=SessionLocal()
    try:
        return service.get_employee_by_department(db,dept)
    finally:
        db.close()



@app.get("/employeesByHighRating",response_model=list[EmployeePerformanceResponse])
def get_employees_with_high_rating():
    db=SessionLocal()
    try:
        return service.get_employees_with_high_rating(db)
    finally:
        db.close()



@app.get("/averageRatingByDepartment")
def avg_rating_by_dept():
    db=SessionLocal()
    try:
        return service.avg_rating_by_dept(db)
    finally:
        db.close()



@app.get("/topFiveEmployees",response_model=list[EmployeePerformanceResponse])
def top_five_employees():
    db=SessionLocal()
    try:
        return service.top_five_employees(db)
    finally:
        db.close()

        

@app.get("/employeesClassification")
def classify_employees():
    db=SessionLocal()
    try:
        return service.classify_employees(db)
    finally:
        db.close()






