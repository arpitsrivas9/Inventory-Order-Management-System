from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    sku = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, default="")
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    order_items = relationship("OrderItem", back_populates="product")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    phone = Column(String(50), default="")

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
