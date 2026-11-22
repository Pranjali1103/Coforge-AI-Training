from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from sqlalchemy.exc import IntegrityError
from models.employeeperformance_model import EmployeePerformance
from schemas.employeeperformance_schema import EmployeePerformanceCreate,EmployeePerformanceUpdate,EmployeePerformanceResponse
from config.logger import logger 

# 1. Create a performance record. 
def create_employee(db:Session,data):
    employee=EmployeePerformance(**data.model_dump())
    db.add(employee)
    try:
        db.commit()
        db.refresh(employee)
        logger.info(f"Employee with Id {employee.employee_id} created successfully")
        return employee
    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate Employee ID")
        raise HTTPException(status_code=409,detail="Employee already exists")
    except Exception:
        db.rollback()
        logger.exception("Unexpected error while creating employee")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 2. List all employee performance records with pagination. 
def get_all_employees(db:Session,skip:int,limit:int):
    try:
        logger.info(f"Fetching employees with skip:{skip} and limit:{limit}")
        query=select(EmployeePerformance).offset(skip).limit(limit)
        employees= db.scalars(query).all()
        logger.info(f"Retrieved {len(employees)} employees successfully")
        return employees
    except Exception:
        logger.exception("Unexpected error occured while fetching employees")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 3. Retrieve a record by employee ID. 
def get_employee_by_id(db:Session,employee_id:int):
    employee=db.get(EmployeePerformance,employee_id)
    if employee is None:
        logger.warning(f"Employee with Id {employee_id} not found")
        raise HTTPException(status_code=404,detail="Employee Not Found")
        
    logger.info(f"Employee with Id {employee_id} retrieved successfully")
    return employee


# 4. Update rating, attendance, and projects completed. 
def update_employee(db:Session,employee_id:int,data):
    employee=get_employee_by_id(db,employee_id)
    for key,value in data.model_dump().items():
        setattr(employee,key,value)
    try:
        db.commit()
        db.refresh(employee)
        logger.info(f"Employee with Id {employee_id} updated successfully")
        return employee
    except IntegrityError:
        db.rollback()
        logger.warning(f"Database constraint violation while updating employee {employee_id}")
        raise
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while updating employee with Id {employee_id}")
        raise HTTPException(status_code=500,detail="Ineternal Server Error")


# 5. Delete a record by employee ID. 
def delete_employee(db:Session,employee_id:int):
    employee=get_employee_by_id(db,employee_id)
    try:
        db.delete(employee)
        db.commit()
        logger.info(f"Employee with Id {employee_id} deleted successfully")
        return True
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while deleting employee with Id {employee_id}")
        raise HTTPException(status_code=500,detail="Ineternal Server Error")


# 6. Filter employees by department. 
def get_employee_by_dept(db:Session,dept:str):
   query=select(EmployeePerformance).where(EmployeePerformance.department==dept)
   employees=db.scalars(query).all()
   if not employees:
       logger.warning(f"No employees found in department {dept}")
       raise HTTPException(status_code=404,detail="No employees found")
   return employees 


# 7. Find employees whose performance rating is at least 4.
def  get_employees_with_high_rating(db:Session):
    query=select(EmployeePerformance).where(EmployeePerformance.performance_rating>=4)
    employees=db.scalars(query).all()
    if not employees:
        logger.warning("No employees with performance  rating>=4 found")
        raise HTTPException(status_code=404,detail="No employees with performance rating >= 4 found")
    logger.info(f"Retrieved {len(employees)} employees with performance rating >=4")
    return employees


# 8. Calculate average performance rating by department. 
def avg_rating_by_dept(db:Session):
    try:
        query=select(EmployeePerformance.department,
                 func.avg(EmployeePerformance.performance_rating)
                 .label("average_rating")).group_by(EmployeePerformance.department)
        ratings=db.execute(query).all()
        result=[]
        for dept,avg_rating in ratings:
            result.append({
                "department":dept,
                "rating":avg_rating
            })
        logger.info(f"Average performance rating by department calculated successfully")
        return result
    except Exception:
        logger.exception("Unexpected error while calculating average performance rating")
        raise HTTPException(status_code=500,detail="Ineternal Server Error")
    

# 9. Return the five highest-rated employees. 
def top_five_employees(db:Session):
    try:
        query=select(EmployeePerformance).order_by(
            EmployeePerformance.performance_rating.desc()).limit(5)
        top_five_emp=db.scalars(query).all()
        logger.info("Successfully retrieved five highest-rated employees.")
        return top_five_emp
    except Exception:
        logger.exception("Unexpected error occured while fetching five highest-rated employees")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 10. Classify employees as Outstanding (4.5 or higher), Good (3.5 to below 4.5), or Needs Improvement (below 3.5). 
def classify_employees(db:Session):
    try:
        employees=db.scalars(select(EmployeePerformance)).all()
        result=[]
        for emp in employees:
            if emp.performance_rating>=4.5:
                category="Outstanding"
            elif emp.performance_rating>=3.5:
                category="Good"
            else:
                category="Needs Improvement"
            result.append({
                "employee_id":emp.employee_id,
                "employee_name":emp.employee_name,
                "performance_rating":emp.performance_rating,
                "category":category
            })
            logger.info(f"{len(employees)} Employees classified successfully")
        return result
    except Exception:
        logger.exception("Unexpected error while classifying employees")
        raise HTTPException(status_code=500,detail="Internal Server Error")



                 

