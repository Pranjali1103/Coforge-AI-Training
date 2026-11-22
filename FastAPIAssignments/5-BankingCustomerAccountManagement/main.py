from fastapi import FastAPI
from config.database import Base,engine,SessionLocal
from schemas.bankcustomer_schema import BankCustomerCreate,BankCustomerResponse,BankCustomerUpdate,AmountUpdate
from services import bankcustomer_service as service

app=FastAPI(title="Banking Customer Account Management API ")

Base.metadata.create_all(bind=engine)


@app.post("/createAccount", response_model=BankCustomerResponse,status_code=201)
def create_customer_account(customer: BankCustomerCreate):
    db=SessionLocal()
    try:
        return service.create_customer_account(db,customer)
    finally:
        db.close()


@app.get("/getAllCustomerAccounts",response_model=list[BankCustomerResponse])
def get_all_customer_accounts(skip:int=0,limit:int=10):
    db = SessionLocal()
    try:
        return service.get_all_customer_accounts(db,skip,limit)
    finally:
        db.close()


@app.get("/getAccountByAccountNumber/{account_number}",response_model=BankCustomerResponse)
def get_account_by_account_number(account_number: str):
    db = SessionLocal()
    try:
        return service.get_account_by_account_number(db,account_number)

    finally:
        db.close()

@app.put("/updateCustomerDetails/{account_number}",response_model=BankCustomerResponse)
def update_customer_details(account_number: str,customer: BankCustomerUpdate):
    db = SessionLocal()
    try:
        return service.update_customer_details(db,account_number,customer)
    finally:
        db.close()

@app.delete("/closeAccount/{account_number}")
def close_account(account_number:str):
    db=SessionLocal()
    try:
        return service.close_account(db,account_number)
    finally:
        db.close()


@app.get( "/getAccountsByBranch/{branch_name}",response_model=list[BankCustomerResponse])
def get_accounts_by_branch( branch_name: str):
    db = SessionLocal()
    try:
        return service.get_accounts_by_branch(db,branch_name)
    finally:
        db.close()

@app.get("/getAccountsByAccountType/{account_type}",response_model=list[BankCustomerResponse])
def get_accounts_by_account_type( account_type: str):
    db = SessionLocal()
    try:
        return service.get_accounts_by_account_type(db,account_type)
    finally:
        db.close()


@app.put("/depositAmount/{account_number}",response_model=BankCustomerResponse)
def deposit_amount(account_number: str,amount_data: AmountUpdate):
    db = SessionLocal()
    try:
        return service.deposit_amount(db,account_number,amount_data.amount)
    finally:
        db.close()


@app.put("/withdrawAmount/{account_number}",response_model=BankCustomerResponse)
def withdraw_amount(account_number: str,amount_data: AmountUpdate):
    db = SessionLocal()
    try:
        return service.withdraw_amount(db,account_number,amount_data.amount)
    finally:
        db.close()

@app.get("/totalDepositsByBranch")
def get_total_deposits_by_branch():
    db = SessionLocal()
    try:
        return service.get_total_deposits_by_branch(db)
    finally:
        db.close()











