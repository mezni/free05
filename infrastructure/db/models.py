"""SQLAlchemy model mappings for bss-core domain entities.

Maps plain Python domain entities to SQLite tables via SQLAlchemy 2.0 Core style.
All models use `Integer` primary keys with UUID strings stored explicitly for
compatibility with the domain layer's UUID type.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    Boolean,
    Numeric,
    ForeignKey,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from infrastructure.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""

    pass


# ──────────────────────────────────────────────────────────────────────
# Customers
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyCustomer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False)
    tier: Mapped[str] = Column(String(20), nullable=False, default="Standard")
    preferences: Mapped[str | None] = Column(Text, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, nullable=False)

    # Back-populated by orders and billing records
    orders = relationship("SqlAlchemyOrder", back_populates="customer", cascade="all, delete-orphan")
    billing_records = relationship("SqlAlchemyBillingRecord", back_populates="customer")

    __table_args__ = (
        UniqueConstraint("email", name="uq_customer_email"),
    )


# ──────────────────────────────────────────────────────────────────────
# Products
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyProduct(Base):
    __tablename__ = "products"

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    sku: Mapped[str] = Column(String(50), unique=True, nullable=False)
    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str | None] = Column(Text, nullable=True)
    unit_price: Mapped[Decimal] = Column(Numeric(10, 2), nullable=False)
    category: Mapped[str | None] = Column(String(100), nullable=True)
    active: Mapped[bool] = Column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime | None] = Column(DateTime, nullable=True)
    updated_at: Mapped[datetime | None] = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("sku", name="uq_product_sku"),
    )


# ──────────────────────────────────────────────────────────────────────
# Inventory
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyInventory(Base):
    __tablename__ = "inventory"

    product_id: Mapped[str] = Column(String(36), ForeignKey("products.id"), primary_key=True)
    stock_quantity: Mapped[int] = Column(Integer, nullable=False, default=0)
    low_stock_threshold: Mapped[int] = Column(Integer, nullable=False, default=5)
    last_updated: Mapped[datetime] = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("product_id", name="uq_inventory_product_id"),
    )


# ──────────────────────────────────────────────────────────────────────
# Orders
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyOrder(Base):
    __tablename__ = "orders"

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id: Mapped[str] = Column(String(36), ForeignKey("customers.id"), nullable=False)
    status: Mapped[str] = Column(String(20), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, nullable=False)

    # Relationships
    customer = relationship("SqlAlchemyCustomer", back_populates="orders")
    items = relationship("SqlAlchemyOrderItem", back_populates="order", cascade="all, delete-orphan")


# ──────────────────────────────────────────────────────────────────────
# Order Items
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyOrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    order_id: Mapped[str] = Column(String(36), ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[str] = Column(String(36), nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = Column(Numeric(10, 2), nullable=False)
    line_total: Mapped[Decimal] = Column(Numeric(12, 2), nullable=False)

    order = relationship("SqlAlchemyOrder", back_populates="items")


# ──────────────────────────────────────────────────────────────────────
# Shipments
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyShipment(Base):
    __tablename__ = "shipments"

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    order_id: Mapped[str] = Column(String(36), ForeignKey("orders.id"), nullable=False)
    tracking_number: Mapped[str] = Column(String(64), unique=True, nullable=False)
    carrier: Mapped[str] = Column(String(20), nullable=False)
    status: Mapped[str] = Column(String(20), nullable=False)
    estimated_delivery_date: Mapped[datetime | None] = Column(DateTime, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("tracking_number", name="uq_shipment_tracking_number"),
    )


# ──────────────────────────────────────────────────────────────────────
# Billing Records
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyBillingRecord(Base):
    __tablename__ = "billing_records"

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id: Mapped[str] = Column(String(36), ForeignKey("customers.id"), nullable=False)
    order_id: Mapped[str | None] = Column(String(36), ForeignKey("orders.id"), nullable=True)
    type: Mapped[str] = Column(String(20), nullable=False)
    amount: Mapped[Decimal] = Column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = Column(String(3), nullable=False, default="USD")
    status: Mapped[str] = Column(String(20), nullable=False)
    payment_method_mask: Mapped[str | None] = Column(String(100), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)

    customer = relationship("SqlAlchemyCustomer", back_populates="billing_records")


# ──────────────────────────────────────────────────────────────────────
# Return Requests
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyReturnRequest(Base):
    __tablename__ = "return_requests"

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    order_item_id: Mapped[str] = Column(String(36), nullable=False)
    rma_number: Mapped[str] = Column(String(36), unique=True, nullable=False)
    reason: Mapped[str] = Column(Text, nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False)
    status: Mapped[str] = Column(String(20), nullable=False)
    shipping_label_url: Mapped[str | None] = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("rma_number", name="uq_return_rma_number"),
    )


# ──────────────────────────────────────────────────────────────────────
# Users
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyUser(Base):
    __tablename__ = "users"

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = Column(String(255), nullable=False)
    role: Mapped[str] = Column(String(20), nullable=False)
    status: Mapped[str] = Column(String(20), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )


# ──────────────────────────────────────────────────────────────────────
# Audit Logs
# ──────────────────────────────────────────────────────────────────────


class SqlAlchemyAuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    actor_user_id: Mapped[str] = Column(String(36), nullable=False)
    operation: Mapped[str] = Column(String(50), nullable=False)
    entity_type: Mapped[str] = Column(String(30), nullable=False)
    entity_id: Mapped[str] = Column(String(36), nullable=False)
    outcome: Mapped[str] = Column(String(50), nullable=False)
    amount: Mapped[Decimal | None] = Column(Numeric(12, 2), nullable=True)
    reason: Mapped[str | None] = Column(Text, nullable=True)
    correlation_id: Mapped[str | None] = Column(String(36), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)