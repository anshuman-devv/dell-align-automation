from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database as database
from services import crud
from schemas import schemas


router = APIRouter()

@router.post("/customers", response_model=schemas.CustomerResponse)
async def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    return crud.create_customer(db, customer)

@router.get("/customers", response_model=list[schemas.CustomerResponse])
async def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

@router.get("/customers/{customer_id}", response_model=schemas.CustomerResponse)
async def read_customer(customer_id: int, db: Session = Depends(database.get_db)):
    customer = crud.get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404)
    return customer

@router.put("/customers/{customer_id}", response_model=schemas.CustomerResponse)
async def update_customer(customer_id: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(database.get_db)):
    customer = crud.update_customer(db, customer_id, customer_update)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, db: Session = Depends(database.get_db)):
    customer = crud.delete_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}


@router.post("/products/", response_model=schemas.ProductResponse)
async def create_product_route(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.create_product(db, product)


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
async def read_product(product_id: int, db: Session = Depends(database.get_db)):
    return crud.get_product(db, product_id)


@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
async def update_product_route(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    return crud.update_product(db, product_id, product)

@router.delete("/products/{product_id}")
async def delete_product_route(product_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_product(db, product_id)

@router.post("/orders/", response_model=schemas.OrderResponse)
async def create_order_route(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    return crud.create_order(db, order)

@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
async def read_order(order_id: int, db: Session = Depends(database.get_db)):
    return crud.get_order(db, order_id)

@router.put("/orders/{order_id}", response_model=schemas.OrderResponse)
async def update_order_route(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(database.get_db)):
    return crud.update_order(db, order_id, order)

@router.delete("/orders/{order_id}")
async def delete_order_route(order_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_order(db, order_id)
