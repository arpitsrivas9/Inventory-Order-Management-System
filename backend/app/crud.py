from decimal import Decimal
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session) -> List[models.Product]:
    return db.query(models.Product).order_by(models.Product.id).all()


def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customers(db: Session) -> List[models.Customer]:
    return db.query(models.Customer).order_by(models.Customer.id).all()


def get_orders(db: Session) -> List[models.Order]:
    return db.query(models.Order).order_by(models.Order.id).all()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    existing = db.query(models.Product).filter(models.Product.sku == product.sku).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product SKU '{product.sku}' already exists.",
        )

    db_product = models.Product(
        name=product.name,
        sku=product.sku,
        description=product.description or "",
        price=Decimal(str(product.price)),
        stock=product.stock,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, updates: schemas.ProductUpdate) -> models.Product:
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if updates.sku and updates.sku != db_product.sku:
        existing = db.query(models.Product).filter(models.Product.sku == updates.sku).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product SKU '{updates.sku}' already exists.",
            )

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    existing = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Customer email '{customer.email}' already exists.",
        )

    db_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone or "",
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    customer = get_customer(db, order.customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")

    if not order.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must include at least one item.")

    product_map = {}
    total_amount = Decimal("0")
    items = []

    for item in order.items:
        product = get_product(db, item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product id {item.product_id} not found.",
            )
        if item.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Insufficient stock for product '{product.name}' (available {product.stock}, requested {item.quantity})."
                ),
            )

        product.stock -= item.quantity
        line_total = Decimal(str(product.price)) * item.quantity
        total_amount += line_total
        items.append((product, item.quantity))
        product_map[item.product_id] = product

    db_order = models.Order(customer_id=customer.id, total_amount=total_amount)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for product, quantity in items:
        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price,
        )
        db.add(order_item)

    db.commit()
    db.refresh(db_order)
    return db_order
