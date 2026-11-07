from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from config.database import Base, engine, SessionLocal
from models.customer_model import Customer
from schema.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)
from services import customer_service as service
from config.logging_config import logger

app = FastAPI(title="Coforge Customer Management API")

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/customerscreate",response_model=CustomerResponse,status_code=201)
def createCustomer(customer:CustomerCreate):
    db=SessionLocal()
    return service.add_customer(db,customer)

@app.get("/")
def home():
    return {"message": "Welcome here"}

@app.get("/getAllCustomers", response_model=list[CustomerResponse])
def getAll():
    logger.info("GetALLCUSTOMERS API called")
    db = SessionLocal()
    try:
        customers=service.get_all_customers(db)
        logger.info(f"Successfully retrieved %s customers {len(customers)}",)
        return customers
    finally:
        db.close()
   

@app.get("/getcustomersbyid/{customerId}",response_model=CustomerResponse)
def getCustomerById(customerId:int):
    db=SessionLocal()
    customer=service.get_customer_by_id(db,customerId)
    return customer

@app.delete("/customerdelete/{customerId}")
def delete(customerId:int):
    db=SessionLocal()
    customer=service.get_customer_by_id(db,customerId)
    db.delete(customer)
    db.commit();
    return "True"


@app.put("/customerupdate/{customerId}")
def update_customer(customerId: int, cust: CustomerCreate):
    db = SessionLocal()
    customer = service.get_customer_by_id(db, customerId)
    customer.customer_name = cust.customer_name
    customer.age = cust.age
    customer.email = cust.email
    customer.department = cust.department
    customer.designation = cust.designation
    db.commit()
    db.refresh(customer)
    return customer


   

