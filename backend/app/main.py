from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Inventory Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Inventory & Order Management API"}


@app.get("/products", response_model=list[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@app.post("/products", response_model=schemas.Product, status_code=201)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@app.put("/products/{product_id}", response_model=schemas.Product)
def edit_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, product)


@app.get("/customers", response_model=list[schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)


@app.post("/customers", response_model=schemas.Customer, status_code=201)
def add_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@app.get("/orders", response_model=list[schemas.Order])
def list_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)


@app.post("/orders", response_model=schemas.Order, status_code=201)
def add_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer
