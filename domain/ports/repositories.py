"""Repository ports (interfaces) for the bss-core Support Application (MVP).

All domain entities depend on these interfaces, not on concrete SQLAlchemy
implementations. Adapters in ``infrastructure/repositories/`` implement these
ports, enabling the SQLite → PostgreSQL migration without domain changes
(NFR‑15/16, principle I).

Each interface mirrors the corresponding entity's CRUD operations and
query methods. Signatures are deliberately minimal — they declare *what* the
domain needs, not *how* data is persisted.
"""

from __future__ import annotations

from uuid import UUID

from ..entities import (
    Customer,
    Inventory,
    Order,
    OrderItem,
    Product,
    ReturnRequest,
    Shipment,
    BillingRecord,
    User,
    AuditLog,
)


# ---------------------------------------------------------------------------
# Customer repository port
# ---------------------------------------------------------------------------


class CustomerRepositoryPort:
    """Port for Customer persistence operations."""

    def get_by_id(self, customer_id: UUID) -> Customer | None: ...

    def get_by_email(self, email: str) -> Customer | None: ...

    def create(self, customer: Customer) -> Customer: ...

    def update(self, customer: Customer) -> Customer: ...

    def delete(self, customer_id: UUID) -> None: ...


# ---------------------------------------------------------------------------
# Product repository port
# ---------------------------------------------------------------------------


class ProductRepositoryPort:
    """Port for Product persistence operations."""

    def get_by_id(self, product_id: UUID) -> Product | None: ...

    def get_by_sku(self, sku: str) -> Product | None: ...

    def get_active(self) -> list[Product]: ...

    def create(self, product: Product) -> Product: ...

    def update(self, product: Product) -> Product: ...

    def delete(self, product_id: UUID) -> None: ...


# ---------------------------------------------------------------------------
# Inventory repository port
# ---------------------------------------------------------------------------


class InventoryRepositoryPort:
    """Port for Inventory persistence operations."""

    def get_by_product_id(self, product_id: UUID) -> Inventory | None: ...

    def create(self, inventory: Inventory) -> Inventory: ...

    def update(self, inventory: Inventory) -> Inventory: ...

    def get_low_stock(self, threshold: int = 10) -> list[Inventory]: ...


# ---------------------------------------------------------------------------
# Order repository port
# ---------------------------------------------------------------------------


class OrderRepositoryPort:
    """Port for Order persistence operations."""

    def get_by_id(self, order_id: UUID) -> Order | None: ...

    def get_by_customer_id(self, customer_id: UUID) -> list[Order]: ...

    def create(self, order: Order) -> Order: ...

    def update(self, order: Order) -> Order: ...

    def delete(self, order_id: UUID) -> None: ...


# ---------------------------------------------------------------------------
# OrderItem repository port
# ---------------------------------------------------------------------------


class OrderItemRepositoryPort:
    """Port for OrderItem persistence operations."""

    def get_by_id(self, item_id: UUID) -> OrderItem | None: ...

    def get_by_order_id(self, order_id: UUID) -> list[OrderItem]: ...

    def create(self, item: OrderItem) -> OrderItem: ...

    def update(self, item: OrderItem) -> OrderItem: ...

    def delete(self, item_id: UUID) -> None: ...


# ---------------------------------------------------------------------------
# Shipment repository port
# ---------------------------------------------------------------------------


class ShipmentRepositoryPort:
    """Port for Shipment persistence operations."""

    def get_by_id(self, shipment_id: UUID) -> Shipment | None: ...

    def get_by_order_id(self, order_id: UUID) -> Shipment | None: ...

    def get_by_tracking(self, tracking_number: str) -> Shipment | None: ...

    def create(self, shipment: Shipment) -> Shipment: ...

    def update(self, shipment: Shipment) -> Shipment: ...


# ---------------------------------------------------------------------------
# BillingRecord repository port
# ---------------------------------------------------------------------------


class BillingRecordRepositoryPort:
    """Port for BillingRecord persistence operations."""

    def get_by_id(self, billing_id: UUID) -> BillingRecord | None: ...

    def get_by_customer_id(self, customer_id: UUID) -> list[BillingRecord]: ...

    def get_by_order_id(self, order_id: UUID | None, customer_id: UUID) -> list[BillingRecord]: ...

    def create(self, record: BillingRecord) -> BillingRecord: ...

    def update(self, record: BillingRecord) -> BillingRecord: ...


# ---------------------------------------------------------------------------
# ReturnRequest repository port
# ---------------------------------------------------------------------------


class ReturnRequestRepositoryPort:
    """Port for ReturnRequest persistence operations."""

    def get_by_id(self, return_id: UUID) -> ReturnRequest | None: ...

    def get_by_order_item_id(self, order_item_id: UUID) -> ReturnRequest | None: ...

    def get_by_rma_number(self, rma_number: str) -> ReturnRequest | None: ...

    def create(self, rma: ReturnRequest) -> ReturnRequest: ...

    def update(self, rma: ReturnRequest) -> ReturnRequest: ...


# ---------------------------------------------------------------------------
# User repository port
# ---------------------------------------------------------------------------


class UserRepositoryPort:
    """Port for User persistence operations."""

    def get_by_id(self, user_id: UUID) -> User | None: ...

    def get_by_email(self, email: str) -> User | None: ...

    def create(self, user: User) -> User: ...

    def update(self, user: User) -> User: ...

    def delete(self, user_id: UUID) -> None: ...

    def search(self, query: str, scope: str = "User Management") -> list[User]: ...


# ---------------------------------------------------------------------------
# AuditLog repository port
# ---------------------------------------------------------------------------


class AuditLogRepositoryPort:
    """Port for AuditLog persistence operations.

    Append‑only: no ``update`` or ``delete`` methods are declared.
    """

    def create(self, log: AuditLog) -> AuditLog: ...

    def get_by_actor(self, actor_user_id: UUID) -> list[AuditLog]: ...

    def get_by_entity(self, entity_type: str, entity_id: UUID) -> list[AuditLog]: ...

    def get_recent(self, limit: int = 100) -> list[AuditLog]: ...


# ---------------------------------------------------------------------------
# Concrete binding hint (non‑port, for documentation only)
# ---------------------------------------------------------------------------

# The concrete implementations live in ``infrastructure/repositories/`` and
# implement exactly these interfaces. Example:
#
# .. code-block:: python
#
#   from domain.ports.repositories import CustomerRepositoryPort
#   from infrastructure.repositories.sqlalchemy_customer import (
#       SqlAlchemyCustomerRepository,
#   )
#
#   repo: CustomerRepositoryPort = SqlAlchemyCustomerRepository(session)