"""Customer routes for bss-core Support Application API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from application.use_cases.customers import (
    create_customer,
    update_customer_tier,
    get_customer_profile,
    list_customers,
    get_customer_by_email,
)
from api.deps import get_current_user_with_scope
from domain.entities import Customer, Tier

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    "",
    status_code=201,
    responses={409: {"description": "Duplicate email or linked records exist"}},
)
async def create_customer_route(
    *,
    name: str,
    email: str,
    tier: Tier = Tier.Standard,
    current_user: dict = Depends(get_current_user_with_scope(["Write"])),
):
    """Create a new customer.

    FR-01: System MUST create, read, update, and delete customers.
    FR-02: System MUST assign a tier of Standard, Gold, or Enterprise.
    FR-21: System MUST retrieve non-sensitive profile details.
    """
    try:
        customer = create_customer(name=name, email=email, tier=tier)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=409, detail="Duplicate email or linked records exist")

    profile = get_customer_profile(customer)
    return {"id": str(customer.id), "name": customer.name, "email": customer.email, "tier": customer.tier, "created_at": profile["created_at"]}


@router.get(
    "",
    response_model=List[dict],
    responses={403: {"description": "Insufficient scope"}},
)
async def list_customers_route(
    *,
    tier: Tier | None = None,
    name_filter: str | None = None,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """List customers with optional tier filter and name search.

    FR-03: System MUST search customers by name or email.
    FR-05: System MUST filter customers by tier.
    """
    customers = list_customers(tier=tier, name_filter=name_filter)
    return [
        {
            "id": str(c.id),
            "name": c.name,
            "email": c.email,
            "tier": c.tier,
        }
        for c in customers
    ]


@router.get(
    "/{customer_id}",
    responses={404: {"description": "Customer not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_customer_route(
    *,
    customer_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get customer by ID.

    FR-01: System MUST create, read, update, and delete customers.
    FR-21: System MUST retrieve non-sensitive profile details.
    """
    # Placeholder - actual lookup via repository
    raise HTTPException(status_code=404, detail="Customer not found")


@router.put(
    "/{customer_id}/tier",
    responses={403: {"description": "Insufficient scope"}, 409: {"description": "Invalid tier transition"}},
)
async def update_customer_tier_route(
    *,
    customer_id: str,
    new_tier: Tier,
    current_user: dict = Depends(get_current_user_with_scope(["Write"])),
):
    """Update customer tier.

    FR-02: System MUST assign a tier of Standard, Gold, or Enterprise.
    """
    # Placeholder - actual lookup and update via repository
    raise HTTPException(status_code=409, detail="Cannot modify customer tier from {}".format(new_tier))


@router.get(
    "/{customer_id}/billing-history",
    responses={404: {"description": "Customer not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_customer_billing_history_route(
    *,
    customer_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get customer billing history.

    FR-04: System MUST show a customer's billing history.
    """
    # Placeholder - actual lookup via repository
    raise HTTPException(status_code=404, detail="Customer not found")


@router.get(
    "/{customer_id}/orders",
    responses={404: {"description": "Customer not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_customer_orders_route(
    *,
    customer_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get customer orders.

    FR-22: System MUST fetch past orders, line items, and fulfillment statuses.
    """
    # Placeholder - actual lookup via repository
    raise HTTPException(status_code=404, detail="Customer not found")