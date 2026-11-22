from fastapi import FastAPI
from config.database import Base,engine,SessionLocal
from schemas.inventoryproduct_schema import InventoryProductCreate,InventoryProductUpdate,InventoryProductResponse,StockUpdate
from services import inventoryproduct_service as service

app=FastAPI(title="Inventory and Product Management API ")


Base.metadata.create_all(bind=engine)

@app.post("/createProduct",response_model=InventoryProductResponse,status_code=201)
def create_product(product:InventoryProductCreate):
    db=SessionLocal()
    try:
        return service.create_product(db,product)
    finally:
        db.close()


@app.get("/getAllProducts", response_model=list[InventoryProductResponse])
def get_all_products(skip:int=0,limit:int=10):
    db=SessionLocal()
    try:
        return service.get_all_products(db,skip,limit)
    finally:
        db.close()


@app.get("/getProductById/{product_id}",response_model=InventoryProductResponse)
def get_product_by_id( product_id: int):
    db = SessionLocal()
    try:
        return service.get_product_by_id(db,product_id)
    finally:
        db.close()


@app.put("/updateProduct/{product_id}", response_model=InventoryProductResponse)
def update_product(product_id: int,product: InventoryProductUpdate):
    db = SessionLocal()
    try:
        return service.update_product(db,product_id,product)
    finally:
        db.close()


@app.delete("/deleteProduct/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    try:
        return service.delete_product(db,product_id)
    finally:
        db.close()


@app.get("/getProductsByCategory/{category}", response_model=list[InventoryProductResponse])
def get_products_by_category(category:str):
    db = SessionLocal()
    try:
        return service.get_products_by_category(db,category)
    finally:
        db.close()

    
@app.get("/lowStockProducts", response_model=list[InventoryProductResponse])
def get_low_stock_products():
    db=SessionLocal()
    try:
        return service.get_low_stock_products(db)
    finally:
        db.close()


@app.put("/increaseStock/{product_id}",response_model=InventoryProductResponse)
def increase_stock(product_id:int,quantity:int):
    db = SessionLocal()
    try:
        return service.increase_stock(db,product_id, quantity)
    finally:
        db.close()


@app.put("/decreaseStock/{product_id}",response_model=InventoryProductResponse)
def decrease_stock(product_id: int, stock: StockUpdate):
    db=SessionLocal()
    try:
        return service.decrease_stock(db,product_id,stock.quantity)
    finally:
        db.close()


@app.get("/inventoryValue")
def get_inventory_value():
    db=SessionLocal()
    try:
        return service.get_inventory_value(db)
    finally:
        db.close()

  
