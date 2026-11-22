from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select,func
from schemas.inventoryproduct_schema import InventoryProductCreate,InventoryProductUpdate
from models.inventoryproduct_model import InventoryProduct
from config.logger import logger

# 1. Add a product. 
def create_product(db:Session,data:InventoryProductCreate):
    product=InventoryProduct(**data.model_dump())
    db.add(product)
    try:
        db.commit()
        db.refresh(product)
        logger.info(f"Product with Id {product.product_id} added successfully")
        return product
    except IntegrityError:
        db.rollback()
        logger.warning( "Duplicate Product ID")
        raise HTTPException(status_code=409,detail="Product already exists")
    except Exception:
        db.rollback()
        logger.exception("Unexpected error while adding product")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 2. List all products with pagination. 
def get_all_products(db:Session,skip:int,limit:int):
    try:
        query=(select(InventoryProduct).offset(skip).limit(limit))
        products=db.scalars(query).all()
        logger.info(f"Successfully retrieved {len(products)} products")
        return products

    except Exception:
        logger.exception( "Unexpected error while fetching products")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 3. Retrieve a product by ID.
def get_product_by_id(db:Session,product_id:int):

     product=db.get(InventoryProduct,product_id)

     if product is None:
         logger.warning(f"Product with Id {product_id} not found")
         raise HTTPException(status_code=404,detail="Product Not Found")

     logger.info(f"Product with Id {product_id} retrieved successfully")
     return product


# 4. Update product information and pricing. 
def update_product(db:Session,product_id:int,data):
    product=get_product_by_id(db,product_id)
    for key,value in data.model_dump().items():
        setattr(product,key,value)
    try:
        db.commit()
        db.refresh(product)
        logger.info(f"Product with Id {product_id} updated successfully")
        return product
    except IntegrityError:
        db.rollback()
        logger.warning(f"Database constraint violation while updating product {product_id}")
        raise 
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while updating product {product_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 5. Delete a product. 
def delete_product(db:Session,product_id:int):
    product=get_product_by_id(db,product_id)
    try:
        db.delete(product)
        db.commit()
        logger.info(f"Product with Id {product_id} deleted successfully")
        return True
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while deleting product with Id {product_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 6. Filter products by category. 
def get_products_by_category(db:Session,category:str):
    query=select(InventoryProduct).where(InventoryProduct.category==category)
    products=db.scalars(query).all()
    
    if not products:
        logger.warning(f"No products found in category {category}")
        raise HTTPException(status_code=404,detail="No products found in this category")
    
    logger.info(f"Retrieved {len(products)} products from category {category}")
    return products


# 7. Find low-stock products where quantity is at or below reorder level.
def get_low_stock_products(db:Session):
    try:
        query=select(InventoryProduct).where(InventoryProduct.quantity_in_stock<=InventoryProduct.reorder_level)
        products=db.scalars(query).all()
        if not products:
            logger.warning("No low-stock products found")
            raise HTTPException(status_code=404,detail="No low-stock products found")
        logger.info(f"Retrieved {len(products)} low-stock products")
        return products

    except HTTPException:
        raise

    except Exception:
        logger.exception( "Unexpected error while fetching low-stock products")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 8. Increase stock by a supplied positive quantity. 
def increase_stock(db:Session,product_id:int,quantity:int):

    if quantity<=0:
        raise HTTPException(status_code=422,detail="Quantity must be greater than 0")
    
    product=get_product_by_id(db,product_id)
    product.quantity_in_stock+=quantity
    try:
        db.commit()
        db.refresh(product)
        logger.info(f"Stock increased for product {product_id} by {quantity}")
        return product
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while increasing stock for product {product_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")

# 9. Decrease stock for an order without allowing negative inventory. 
def decrease_stock(db:Session,product_id:int,quantity:int):
    product=get_product_by_id(db,product_id)

    if product.quantity_in_stock < quantity:
        logger.warning(f"Insufficient stock for product {product_id}")
        raise HTTPException(status_code=400,detail="Insufficient stock available")
    
    product.quantity_in_stock -= quantity
    
    try:
        db.commit()
        db.refresh(product)
        logger.info(f"Stock decreased for product {product_id} by {quantity}")
        return product
    
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while decreasing stock for product {product_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")

# 10. Calculate total inventory value and inventory value by category. 
def get_inventory_value(db:Session):
    try:
        total_inventory_value=db.scalar(
            select(func.sum(InventoryProduct.unit_price*InventoryProduct.quantity_in_stock))
        )

        category_values=db.execute(
            select(InventoryProduct.category,func.sum(InventoryProduct.unit_price*
                                                      InventoryProduct.quantity_in_stock)
                                                      .label("inventory_value"))
            .group_by(InventoryProduct.category)
        ).all()

        category_result = []
        for category,value in category_values:
            category_result.append({
                "category": category,
                "inventory_value":value
            })

        logger.info("Inventory value calculated successfully")
        return {
            "total_inventory_value":total_inventory_value,
            "category_wise_inventory_value":category_result
        }

    except Exception:
        logger.exception("Unexpected error while calculating inventory value")
        raise HTTPException(status_code=500,detail="Internal Server Error")