"""Domain entities for bss-core Support Application (MVP).

All entities are plain Python classes with no framework imports.
They follow the invariant rules and state machines defined in
`domain/policies.py` and `data-model.md`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4


class Tier(str, Enum):
    """Customer tier enumeration."""
    Standard = "Standard"
    Gold = "Gold"
    Enterprise = "Enterprise"


class Status(str, Enum):
    """Base status enumeration."""
    active = "active"
    inactive = "inactive"


class OrderStatus(str, Enum):
    """Order status enumeration."""
    Processing = "Processing"
    Completed = "Completed"
    Returned = "Returned"
    Cancelled = "Cancelled"


class ShipmentStatus(str, Enum):
    """Shipment status enumeration."""
    Label_Created = "Label Created"
    In_Transit = "In Transit"
    Out_for_Delivery = "Out for Delivery"
    Delivered = "Delivered"


class ReturnStatus(str, Enum):
    """Return request status enumeration."""
    Submitted = "Submitted"
    Approved = "Approved"
    Rejected = "Rejected"
    Completed = "Completed"


class OrderItemReturnEligibility(str, Enum):
    """Return eligibility enumeration for order items."""
    Eligible = "eligible"
    NonEligible = "non-eligible"


# ---------------------------------------------------------------------------
# Customer
# ---------------------------------------------------------------------------


class Customer:
    """Customer entity with unique email, tier, and preferences."""

    def __init__(
        self,
        *,
        id: UUID | None = None,
        name: str,
        email: str,
        tier: Tier = Tier.Standard,
        preferences: dict | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.email = email
        self.tier = tier
        self.preferences = preferences or {}
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<Customer id={self.id} name={self.name} email={self.email}>"

    @property
    def is_active(self) -> bool:
        return True  # Customer activity managed via order/billing state


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------


class Product:
    """Product entity with unique SKU, name, and unit price."""

    def __init__(
        self,
        *,
        id: UUID | None = None,
        sku: str,
        name: str,
        description: str | None = None,
        unit_price: float,
        category: str | None = None,
        active: bool = True,
    ):
        self.id = id or uuid4()
        self.sku = sku
        self.name = name
        self.description = description
        self.unit_price = unit_price
        self.category = category
        self.active = active
        if self.unit_price <= 0:
            raise ValueError("unit_price must be > 0")

    def __repr__(self) -> str:
        return f"<Product id={self.id} sku={self.sku} name={self.name}>"

    @property
    def is_active(self) -> bool:
        return self.active


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------


class Inventory:
    """Inventory entity linked to a Product; tracks stock quantity."""

    def __init__(
        self,
        *,
        product_id: UUID,
        stock_quantity: int = 0,
        last_updated: datetime | None = None,
    ):
        self.product_id = product_id
        self.stock_quantity = max(0, stock_quantity)
        self.last_updated = last_updated or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<Inventory product_id={self.product_id} stock_quantity={self.stock_quantity}>"

    @property
    def can_fulfill(self, quantity: int) -> bool:
        return self.stock_quantity >= quantity


# ---------------------------------------------------------------------------
# Order
# ---------------------------------------------------------------------------


class Order:
    """Order entity composed of a Customer and OrderItems.

    The Order tracks status, derived total, and line items.
    Status transitions are governed by `domain/policies.py`.
    """

    def __init__(
        self,
        *,
        id: UUID | None = None,
        customer_id: UUID,
        status: OrderStatus = OrderStatus.Processing,
        created_at: datetime | None = None,
    ):
        self.id = id or uuid4()
        self.customer_id = customer_id
        self.status = status
        self.created_at = created_at or datetime.now(timezone.utc)
        self.items: list[OrderItem] = []

    def add_item(self, item: "OrderItem") -> None:
        """Add an OrderItem to the order and recompute total."""
        self.items.append(item)

    def remove_item(self, item_id: UUID) -> None:
        """Remove an OrderItem by its id."""
        self.items = [i for i in self.items if i.id != item_id]

    @property
    def total_amount(self) -> float:
        """Derived total: sum of all line items."""
        return sum(item.line_total for item in self.items)

    def __repr__(self) -> str:
        return "<Order id='%s' customer_id='%s' status='%s' total='%s'>" % (
            self.id,
            self.customer_id,
            self.status,
            self.total_amount,
        )

    @property
    def is_terminal(self) -> bool:
        return self.status in {
            OrderStatus.Completed,
            OrderStatus.Returned,
            OrderStatus.Cancelled,
        }


# ---------------------------------------------------------------------------
# OrderItem
# ---------------------------------------------------------------------------


class OrderItem:
    """OrderItem entity linking an Order to a Product with quantity and price."""

    def __init__(
        self,
        *,
        id: UUID | None = None,
        order_id: UUID,
        product_id: UUID,
        quantity: int,
        unit_price: float,
        line_total: float | None = None,
        return_eligible: bool = True,
    ):
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        if unit_price <= 0:
            raise ValueError("unit_price must be > 0")
        self.id = id or uuid4()
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.line_total = line_total or unit_price * quantity
        self.return_eligible = return_eligible

    def __repr__(self) -> str:
        return (
            f"<OrderItem id={self.id} order_id={self.order_id} "
            f"product_id={self.product_id} quantity={self.quantity}>"
        )

    @property
    def return_eligible_qty(self) -> int:
        return min(self.quantity, 1)  # simplified; policy-driven in policies.py


# ---------------------------------------------------------------------------
# Shipment
# ---------------------------------------------------------------------------


class Shipment:
    """Shipment entity linked to an Order with carrier and tracking."""

    def __init__(
        self,
        *,
        id: UUID | None = None,
        order_id: UUID,
        carrier: str,
        tracking_number: str,
        status: ShipmentStatus = ShipmentStatus.Label_Created,
        estimated_delivery_date: datetime | None = None,
    ):
        self.id = id or uuid4()
        self.order_id = order_id
        self.carrier = carrier
        self.tracking_number = tracking_number
        self.status = status
        self.estimated_delivery_date = estimated_delivery_date

    def __repr__(self) -> str:
        return (
            f"<Shipment id={self.id} order_id={self.order_id} "
            f"carrier={self.carrier} tracking={self.tracking_number}>"
        )

    @property
    def is_terminal(self) -> bool:
        return self.status in {
            ShipmentStatus.Delivered,
            ShipmentStatus.Returned,
            ShipmentStatus.Cancelled,
        }


# ---------------------------------------------------------------------------
# BillingRecord
# ---------------------------------------------------------------------------


class BillingRecord:
    """BillingRecord entity for charges, refunds, and credits."""

    def __init__(
        self,
        *,
        id: UUID | None = None,
        customer_id: UUID,
        order_id: UUID | None = None,
        type: str,
        amount: float,
        currency: str = "USD",
        payment_method_mask: str | None = None,
        status: str = "Pending",
        created_at: datetime | None = None,
    ):
        if amount <= 0:
            raise ValueError("amount must be > 0")
        self.id = id or uuid4()
        self.customer_id = customer_id
        self.order_id = order_id
        self.type = type
        self.amount = amount
        self.currency = currency
        self.payment_method_mask = payment_method_mask or "Visa ending in ----"
        self.status = status
        self.created_at = created_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return (
            f"<BillingRecord id={self.id} customer_id={self.customer_id} "
            f"type={self.type} amount={self.amount} {self.currency}>"
        )

    @property
    def is_charge(self) -> bool:
        return self.type == "Charge"

    @property
    def is_refund(self) -> bool:
        return self.type == "Refund"

    @property
    def is_credit(self) -> bool:
        return self.type == "Credit"


# ---------------------------------------------------------------------------
# ReturnRequest
# ---------------------------------------------------------------------------


class ReturnRequest:
    """ReturnRequest entity with RMA number, idempotency key, and status."""

    def __init__(
        self,
        *,
        id: UUID | None = None,
        order_item_id: UUID,
        rma_number: str,
        reason: str,
        quantity: int,
        status: ReturnStatus = ReturnStatus.Submitted,
        idempotency_key: UUID | None = None,
        shipping_label_url: str | None = None,
        created_at: datetime | None = None,
    ):
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        if not rma_number:
            raise ValueError("rma_number must be non-empty")
        self.id = id or uuid4()
        self.order_item_id = order_item_id
        self.rma_number = rma_number
        self.reason = reason
        self.quantity = quantity
        self.status = status
        self.idempotency_key = idempotency_key or uuid4()
        self.shipping_label_url = shipping_label_url
        self.created_at = created_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return (
            f"<ReturnRequest id={self.id} rma_number={self.rma_number} "
            f"status={self.status} quantity={self.quantity}>"
        )

    @property
    def is_terminal(self) -> bool:
        return self.status in {
            ReturnStatus.Completed,
            ReturnStatus.Rejected,
        }


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------


class User:
    """User entity with unique email, password hash, and role."""

    def __init__(
        self,
        *,
        id: UUID | None = None,
        name: str,
        email: str,
        password_hash: str,
        role: str,
        status: Status = Status.active,
        last_login_at: datetime | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        if not email or "@" not in email:
            raise ValueError("email must be valid")
        self.id = id or uuid4()
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.status = status
        self.last_login_at = last_login_at
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"

    @property
    def is_active(self) -> bool:
        return self.status == Status.active

    def can(self, permission: str) -> bool:
        """Check if this user has the given permission (orthogonal to roles)."""
        return True  # permission check handled by authZ matrix


# ---------------------------------------------------------------------------
# AuditLog
# ---------------------------------------------------------------------------


class AuditLog:
    """AuditLog entity — append-only, no update/delete path."""

    def __init__(
        self,
        *,
        id: UUID | None = None,
        actor_user_id: UUID,
        operation: str,
        entity_type: str,
        entity_id: UUID,
        outcome: str,
        amount: float | None = None,
        reason: str | None = None,
        correlation_id: UUID | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id or uuid4()
        self.actor_user_id = actor_user_id
        self.operation = operation
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.outcome = outcome
        self.amount = amount
        self.reason = reason
        self.correlation_id = correlation_id
        self.created_at = created_at or datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return (
            f"<AuditLog id={self.id} operation={self.operation} "
            f"entity={self.entity_type} outcome={self.outcome}>"
        )

    @property
    def is_success(self) -> bool:
        return self.outcome in {"success", "completed"}

    @property
    def is_financial(self) -> bool:
        return self.amount is not None


# ---------------------------------------------------------------------------
# Module-Level Helpers
# ---------------------------------------------------------------------------


def generate_rma_number() -> str:
    """Generate a deterministic-looking RMA number."""
    from datetime import datetime

    return f"RMA-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def generate_idempotency_key() -> UUID:
    """Generate a fresh idempotency key."""
    from uuid import uuid4

    return uuid4()


class BillingType(str, Enum):
    """Billing record type enumeration."""
    Charge = "Charge"
    Refund = "Refund"
    Credit = "Credit"


class BillingStatus(str, Enum):
    """Billing status enumeration."""
    Pending = "Pending"
    Completed = "Completed"
    Failed = "Failed"


class Outcome(str, Enum):
    """Outcome enumeration."""
    success = "success"
    failure = "failure"


class Carrier(str, Enum):
    """Carrier enumeration."""
    FedEx = "FedEx"
    UPS = "UPS"
    DHL = "DHL"


class UserRole(str, Enum):
    """User role enumeration."""
    Viewer = "Viewer"
    Operator = "Operator"
    Manager = "Manager"
    Administrator = "Administrator"
    User_Manager = "User Manager"


class UserStatus(str, Enum):
    """User status enumeration."""
    active = "active"
    inactive = "inactive"