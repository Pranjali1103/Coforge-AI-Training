from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from config.database import Base,engine,SessionLocal
from models.employee_model import Employee
from schemas.employee_schema import EmployeeCreate,EmployeeResponse,EmployeeUpdate

from services import employee_service as service

app=FastAPI(title="Welcome to FastAPi Project")

#create database tables
Base.metadata.create_all(bind=engine)


@app.post("/employeecreate",response_model=EmployeeResponse)
def createEmployee(employee:EmployeeCreate):
    db=SessionLocal()
    return service.add_employee(db,employee)

@app.get("/getAllEmployees",response_model=list[EmployeeResponse])
def getAll():
    db=SessionLocal()
    return service.get_all_employees(db)

@app.get("/getEmployeeById/{employeeId}",response_model=EmployeeResponse)
def getEmployeeById(employeeId:int):
    db=SessionLocal()
    employee=service.get_employee_by_id(db,employeeId)
    return employee

@app.put("/employeeupdate/{employeeId}",response_model=EmployeeResponse)
def updateEmployee(employeeId:int,emp:EmployeeUpdate):
    db=SessionLocal()
    try:
        return service.update_employee(db,employeeId,emp)
    finally:
        db.close()

@app.delete("/employeedelete/{employeeId}")
def deleteEmployee(employeeId:int):
    db=SessionLocal()
    try:
        service.delete_employee(db,employeeId)
    finally:
        db.close()

