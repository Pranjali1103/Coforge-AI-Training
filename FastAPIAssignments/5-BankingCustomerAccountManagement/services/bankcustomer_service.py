from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select,func
from models.bankcustomer_model import BankCustomer
from schemas.bankcustomer_schema import BankCustomerCreate,BankCustomerUpdate
from config.logger import logger
from decimal import Decimal


# 1. Open a customer account.
def create_customer_account(db:Session,data:BankCustomerCreate):
    customer = BankCustomer(**data.model_dump())
    db.add(customer)
    try:
        db.commit()
        db.refresh(customer)
        logger.info(f"Customer with Id {customer.customer_id} account opened successfully")
        return customer
    
    except IntegrityError:
        db.rollback()
        logger.warning(  "Duplicate account number or email detected")
        raise HTTPException(status_code=409,detail="Account number or email already exists")
    
    except Exception:
        db.rollback()
        logger.exception("Unexpected error while opening customer account")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 2. List customer accounts with pagination. 
def get_all_customer_accounts(db:Session,skip:int,limit:int):
    try:
        query=(select(BankCustomer).offset(skip).limit(limit))
        customers=db.scalars(query).all()
        logger.info(f"Successfully retrieved {len(customers)} customers accounts")
        return customers
    except Exception:
        logger.exception("Unexpected error while fetching customer accounts")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 3. Retrieve an account by account number. 
def get_account_by_account_number(db: Session,account_number: str):
    query = select(BankCustomer).where(BankCustomer.account_number == account_number)
    customer = db.scalar(query)
    if customer is None:
        logger.warning(f"Account {account_number} not found")
        raise HTTPException(status_code=404,detail="Account Not Found")
    logger.info(f"Account {account_number} retrieved successfully")
    return customer
    

# 4. Update customer contact or branch details. 
def update_customer_details(db: Session,account_number: str, data: BankCustomerUpdate):
    customer = get_account_by_account_number(db,account_number)
    for key, value in data.model_dump().items():
        setattr(customer,key,value)

    try:
        db.commit()
        db.refresh(customer)
        logger.info(f"Customer details updated successfully for account {account_number}")
        return customer
    except IntegrityError:
        db.rollback()
        logger.warning(f"Duplicate email while updating account {account_number}")
        raise HTTPException(status_code=409,detail="Email already exists")
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while updating account {account_number}")
        raise HTTPException(status_code=500,detail="Internal Server Error")
    

# 5. Close an account only if balance is zero. 
def close_account(db: Session,account_number: str):
    customer = get_account_by_account_number(db,account_number)
    if customer.balance>0:
        logger.warning(  f"Attempt to close account {account_number} with non-zero balance")
        raise HTTPException(status_code=409,detail="Account can only be closed when balance is zero")
    try:
        db.delete(customer)
        db.commit()
        logger.info(f"Account {account_number} closed successfully")
        return True
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while closing account {account_number}")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 6. Filter accounts by branch. 
def get_accounts_by_branch(db: Session, branch_name: str):
    query = select(BankCustomer).where(BankCustomer.branch_name == branch_name)
    customers = db.scalars(query).all()
    if not customers:
        logger.warning( f"No accounts found in branch {branch_name}")
        raise HTTPException(status_code=404,detail="No accounts found in this branch")
    logger.info( f"Retrieved {len(customers)} accounts from branch {branch_name}")
    return customers

# 7. Filter accounts by account type. 
def get_accounts_by_account_type(db: Session, account_type: str):
    query = select(BankCustomer).where(BankCustomer.account_type == account_type)
    customers = db.scalars(query).all()
    if not customers:
        logger.warning(f"No accounts found with type {account_type}")
        raise HTTPException(status_code=404,detail="No accounts found for this account type")
    logger.info( f"Retrieved {len(customers)} {account_type} accounts")
    return customers


# 8. Deposit a positive amount into an active account. 
def deposit_amount(db: Session,account_number: str,amount:Decimal):
    customer = get_account_by_account_number(db,account_number)
    if not customer.is_active:
        logger.warning(f"Deposit attempted on inactive account {account_number}")
        raise HTTPException(status_code=409, detail="Cannot transact on an inactive account")
    customer.balance += amount
    try:
        db.commit()
        db.refresh(customer)
        logger.info(f"Deposited {amount} into account {account_number}")
        return customer
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while depositing into account {account_number}")
        raise HTTPException(status_code=500,detail="Internal Server Error")
    

# 9. Withdraw a positive amount without overdrawing. 
def withdraw_amount(db:Session,account_number:str,amount:Decimal):
    customer = get_account_by_account_number(db,account_number)
    if not customer.is_active:
            logger.warning(f"Withdrawal attempted on inactive account {account_number}")
            raise HTTPException(status_code=409, detail="Cannot transact on an inactive account")
    if customer.balance < amount:
        logger.warning(f"Insufficient balancr in account {account_number}")
        raise HTTPException(status_code=409,detail="Insufficient balance")
    customer.balance -= amount
    try:
        db.commit()
        db.refresh(customer)
        logger.info(f"Withdrew {amount} from account {account_number}")
        return customer
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while withdrawing from account {account_number}")
        raise HTTPException(status_code=500,detail="Internal Server Error")
    

# 10. Calculate total deposits held by each branch.
def get_total_deposits_by_branch(db:Session):
    try:
        query=(select(BankCustomer.branch_name,func.sum(BankCustomer.balance).label("total_deposits"))
              .group_by( BankCustomer.branch_name))
        branches = db.execute(query).all()
        result=[]
        for branch,total in branches:
            result.append(
                {
                "branch_name": branch,
                "total_deposits":total
                }
            )
        logger.info(f"Calculated total deposits for {len(result)} branches")
        return result
    except Exception:
        logger.exception( "Unexpected error while calculating branch deposits")
        raise HTTPException(status_code=500,detail="Internal Server Error")

        