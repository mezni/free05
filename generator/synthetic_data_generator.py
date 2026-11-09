"""Deterministic synthetic data generator for bss-core Support Application.

Generates a reproducible demo/exhibition dataset exercising every entity and flow
end-to-end. Invoked via:

    python -m generator.synthetic_data_generator --seed 20261108 --out docs/prototype/generator/output
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Constants / profiles
# ---------------------------------------------------------------------------

CUSTOMER_TIERS = ["Standard", "Gold", "Enterprise"]
ORDER_STATUSES = ["Processing", "Completed", "Returned", "Cancelled"]
SHIPMENT_STATUSES = ["Delivered", "Out for Delivery", "In Transit", "Label Created"]
BILLING_TYPES = ["Charge", "Refund", "Credit"]
BILLING_STATUSES = ["Completed", "Pending", "Failed"]
USER_ROLES = ["Viewer", "Operator", "Manager", "Administrator", "User Manager"]
DEMO_PASSWORD_HASH = "$2b$12$KjxOlJJJJJJJJJJJJJJJJ."  # pre-hashed demo value


def _hash_password(password: str) -> str:
    """Return a pre-hashed password (bcrypt-compatible format for demo purposes)."""
    # In MVP we just return a deterministic hash placeholder;
    # real hashing done by infrastructure.
    return DEMO_PASSWORD_HASH


# ---------------------------------------------------------------------------
# RNG helpers
# ---------------------------------------------------------------------------


def _make_rng(seed: int) -> random.Random:
    return random.Random(seed)


def _choice(rng: random.Random, items: List[str]) -> str:
    return rng.choice(items)


def _float_rng(rng: random.Random) -> float:
    return rng.random() * 200  # up to $200


def _int_rng(rng: random.Random, minimum: int, maximum: int) -> int:
    return rng.randint(minimum, maximum)


# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------

def _gen_customers(rng: random.Random, n: int) -> List[Dict[str, Any]]:
    customers = []
    tier_weights = [0.6, 0.3, 0.1]  # Standard/Gold/Enterprise
    for i in range(n):
        customer_id = f"cust_{i+1:03d}"
        name = f"Customer {customer_id}"
        # Deterministic email based on ID and tier
        tier = _choice(rng, CUSTOMER_TIERS)
        email = f"contact_{customer_id}@example.com"
        # For Gold/Enterprise, add suffix
        if tier == "Gold":
            email = f"gold_{customer_id}@example.com"
        elif tier == "Enterprise":
            email = f"enterprise_{customer_id}@example.com"
        customers.append({
            "id": customer_id,
            "name": name,
            "email": email,
            "tier": tier,
            "created_at": (datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 30))).isoformat() + "Z",
        })
    return customers


def _gen_products(rng: random.Random, n: int) -> List[Dict[str, Any]]:
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Food & Beverage"]
    products = []
    for i in range(n):
        product_id = f"prod_{i+1:03d}"
        name = f"Product {product_id}"
        category = _choice(rng, categories)
        unit_price = Decimal(str(round(_float_rng(rng) * 100 + 5, 2)))  # $5-$205
        # 10% inactive
        inactive = rng.random() < 0.1
        products.append({
            "id": product_id,
            "name": name,
            "category": category,
            "unit_price": str(unit_price),
            "inactive": inactive,
            "created_at": (datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 30))).isoformat() + "Z",
        })
    return products


def _gen_inventory(rng: random.Random, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    inventory = []
    for p in products:
        pid = p["id"]
        quantity = rng.randint(10, 200)
        low_stock_threshold = rng.randint(3, 10)
        inventory.append({
            "product_id": pid,
            "quantity": quantity,
            "low_stock_threshold": low_stock_threshold,
            "status": "out-of-stock" if quantity <= low_stock_threshold else "in-stock",
        })
    return inventory


def _gen_orders(
    rng: random.Random,
    customers: List[Dict[str, Any]],
    products: List[Dict[str, Any]],
    n: int,
) -> List[Dict[str, Any]]:
    # Map product IDs to products for quick lookup
    product_map = {p["id"]: p for p in products}
    orders = []
    for i in range(n):
        customer = rng.choice(customers)
        customer_id = customer["id"]
        # 1-5 order items, typical 1-3
        n_items = rng.randint(1, 5)
        items = []
        total = Decimal("0")
        for _ in range(n_items):
            product = rng.choice(products)
            qty = rng.randint(1, 5)
            unit_price = Decimal(product["unit_price"])
            line_total = qty * unit_price
            total += line_total
            items.append({
                "product_id": product["id"],
                "quantity": qty,
                "unit_price": str(unit_price),
                "line_total": str(line_total),
            })
        # Determine order status based on weights
        r = rng.random()
        if r < 0.20:
            status = "Processing"
        elif r < 0.20 + 0.55:
            status = "Completed"
        elif r < 0.20 + 0.55 + 0.15:
            status = "Returned"
        else:
            status = "Cancelled"
        order_id = f"ord_{i+1:04d}"
        orders.append({
            "id": order_id,
            "customer_id": customer_id,
            "status": status,
            "items": items,
            "total_amount": str(total.quantize(Decimal("0.01"))),
            "created_at": (datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 90))).isoformat() + "Z",
        })
    return orders


def _gen_shipments(
    rng: random.Random, orders: List[Dict[str, Any]], n: int
) -> List[Dict[str, Any]]:
    # 1 shipment per completed order
    completed = [o for o in orders if o["status"] == "Completed"]
    shipments = []
    for i, order in enumerate(completed[:n]):
        shipment_id = f"shp_{order['id']}"
        carrier = _choice(rng, ["FedEx", "UPS", "DHL"])
        # ETA is order created + some days
        eta_days = rng.randint(3, 14)
        eta = (datetime.fromisoformat(order["created_at"].replace("Z", "+00:00")) +
               timedelta(days=eta_days)).date().isoformat()
        shipments.append({
            "id": shipment_id,
            "order_id": order["id"],
            "tracking_number": f"TRK-{order['id']}-{i+1:03d}",
            "carrier": carrier,
            "status": _choice(rng, SHIPMENT_STATUSES),
            "estimated_delivery_date": eta,
            "created_at": order["created_at"],
        })
    return shipments


def _gen_billing_records(
    rng: random.Random, orders: List[Dict[str, Any]], customers: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    records = []
    # 1-3 billing records per order
    for order in orders:
        customer = next(c for c in customers if c["id"] == order["customer_id"])
        n_records = rng.randint(1, 3)
        for _ in range(n_records):
            billing_type = _choice(rng, BILLING_TYPES)
            # Determine amount based on type
            if billing_type == "Charge":
                amount = Decimal(str(round(_float_rng(rng) * 100 + 10, 2)))  # $10-$210
            elif billing_type == "Refund":
                amount = Decimal(str(round(_float_rng(rng) * 50 + 5, 2)))  # $5-$55
            else:
                amount = Decimal(str(round(_float_rng(rng) * 20 + 1, 2)))  # $1-$21
            amount = amount.quantize(Decimal("0.01"))
            currency = "USD"
            rtype = billing_type
            status = _choice(rng, BILLING_STATUSES)
            records.append({
                "id": f"bill_{len(records)+1:04d}",
                "customer_id": order["customer_id"],
                "order_id": order["id"],
                "type": rtype,
                "amount": str(amount),
                "currency": currency,
                "status": status,
                "payment_method_mask": f"Masked-{_choice(rng, ['Visa', 'MC', 'AX', 'Disc'])}-ending-in-{rng.randint(1000, 9999)}",
                "created_at": (datetime.fromisoformat(order["created_at"].replace("Z", "+00:00")) +
                               timedelta(days=rng.randint(0, 3))).isoformat() + "Z",
            })
    return records


def _gen_return_requests(
    rng: random.Random, orders: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    # 10-20% of order items eligible
    eligible_items = []
    for order in orders:
        for item in order.get("items", [])[:3]:  # limit to first 3 items per order
            if rng.random() < 0.15:  # ~15% eligibility
                eligible_items.append({
                    "order_item_id": order["id"],
                    "quantity": item["quantity"],
                })
    return_requests = []
    for i, ei in enumerate(eligible_items[:rng.randint(50, 100)]):

        rma_number = f"RMA-{ei['order_item_id']}-{i+1:03d}"
        reason = rng.choice([
            "Item defective", "Wrong item received", "Changed my mind",
            "Quality issue", "Duplicate order"
        ])
        return_requests.append({
            "id": f"req_{i+1:04d}",
            "rma_number": rma_number,
            "order_item_id": ei["order_item_id"],
            "quantity": ei["quantity"],
            "reason": reason,
            "status": rng.choice(["Submitted", "Approved", "Rejected", "Completed"]),
            "created_at": (datetime(2026, 6, 1) + timedelta(days=rng.randint(0, 60))).isoformat() + "Z",
            "shipping_label_url": f"https://shipping.example.com/labels/{rma_number}.pdf",
        })
    return return_requests


def _gen_users(rng: random.Random, n: int) -> List[Dict[str, Any]]:
    """Generate exactly n users deterministically."""
    users = []
    USER_ROLES = ["Viewer", "Operator", "Manager", "Administrator", "User Manager"]
    # Place one of each role, then fill remaining slots
    base_users = 5  # one per role
    extra = n - base_users
    if extra > 0:
        # Add extra users, cycling through roles
        for i in range(extra):
            role = USER_ROLES[i % len(USER_ROLES)]
            user_id = f"usr_{base_users + i + 1:03d}"
            name = f"User {user_id}"
            email = f"user_{user_id}@example.com"
            status = "active"  # fixed, no rng
            users.append({
                "id": user_id,
                "name": name,
                "email": email,
                "role": role,
                "status": status,
                "password_hash": _hash_password("demo-pass-123"),
                "created_at": (datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 90))).isoformat() + "Z",
            })
    # Add the base users (one per role)
    for i, role in enumerate(USER_ROLES):
        user_id = f"usr_{i+1:03d}"
        name = f"User {user_id}"
        email = f"user_{user_id}@example.com"
        status = "active"
        users.append({
            "id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "status": status,
            "password_hash": _hash_password("demo-pass-123"),
            "created_at": (datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 90))).isoformat() + "Z",
        })
    # Shuffle using rng for determinism
    rng.shuffle(users)
    return users


def _gen_audit_logs(
    rng: random.Random, customers: List[Dict[str, Any]], orders: List[Dict[str, Any]],
    users: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    entries = []
    # One entry per refund + per user mutation
    # Add refund entries
    billing_count = len([o for o in orders])  # rough estimate
    for i in range(min(20, billing_count)):
        entries.append({
            "id": f"aud_{i+1:04d}",
            "actor_user_id": rng.choice([u["id"] for u in users]),
            "operation": rng.choice(["create_customer", "create_order", "create_billing", "create_return"]),
            "entity_type": rng.choice(["customer", "order", "billing_record", "return_request"]),
            "entity_id": rng.choice([c["id"] for c in customers] + [o["id"] for o in orders]),
            "amount": str(Decimal(str(round(_float_rng(rng) * 100, 2))).quantize(Decimal("0.01"))),
            "created_at": (datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 365))).isoformat() + "Z",
        })
    # Add user mutation entries
    for u in users[:10]:
        entries.append({
            "id": f"aud_{len(entries)+1:04d}",
            "actor_user_id": u["id"],
            "operation": "update_user_status",
            "entity_type": "user",
            "entity_id": u["id"],
            "amount": None,
            "created_at": (datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 365))).isoformat() + "Z",
        })
    return entries


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------


def generate_synthetic_data(seed: int = 20261108, out_dir: str = "docs/prototype/generator/output") -> Dict[str, int]:
    """Generate the full synthetic dataset.

    Args:
        seed: Deterministic seed (default: 20261108).
        out_dir: Output directory for JSON files.

    Returns:
        Dict of row counts per entity.
    """
    rng = _make_rng(seed)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Fixed user count within target range; shuffle for determinism
    n_users = 15  # within 10-20 target range

    print(f"Generating synthetic data (seed={seed})")
    print(f"  Customers: estimated 50-100")
    print(f"  Products: estimated 30-60")
    print(f"  Orders: estimated 200-500")

    # Generate entities
    customers = _gen_customers(rng, 70)
    products = _gen_products(rng, 44)
    inventory = _gen_inventory(rng, products)
    orders = _gen_orders(rng, customers, products, 314)

    print(f"  Shipments (≈completed orders): {min(50, sum(1 for o in orders if o['status'] == 'Completed'))}")
    shipments = _gen_shipments(rng, orders, min(50, sum(1 for o in orders if o['status'] == 'Completed')))

    print(f"  Billing records: {sum(rng.randint(1, 3) for _ in orders)}")
    billing_records = _gen_billing_records(rng, orders, customers)

    print(f"  Return requests: {len(_gen_return_requests(rng, orders))}")
    return_requests = _gen_return_requests(rng, orders)

    users = _gen_users(rng, n_users)
    audit_logs = _gen_audit_logs(rng, customers, orders, users)

    # Write JSON files
    def _write(name: str, data: List[Dict[str, Any]]) -> int:
        filepath = out_path / f"{name}.json"
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  Wrote {name}.json: {len(data)} records")
        return len(data)

    counts = {
        "customers": _write("customers", customers),
        "products": _write("products", products),
        "inventory": _write("inventory", inventory),
        "orders": _write("orders", orders),
        "shipments": _write("shipments", shipments),
        "billing_records": _write("billing_records", billing_records),
        "return_requests": _write("return_requests", return_requests),
        "users": _write("users", users),
        "audit_logs": _write("audit_logs", audit_logs),
    }

    # Write manifest
    seed_hash = int(hashlib.sha256(str(seed).encode()).hexdigest()[:8], 16)
    base = datetime(2026, 1, 1)
    generated = base + timedelta(days=seed_hash % 365)
    manifest = {
        "seed": seed,
        "version": "1.0.0",
        "generated_at": generated.isoformat(),
        "counts": counts,
    }
    manifest_path = out_path / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, default=str)
    print(f"  Wrote manifest.json with counts: {counts}")

    return counts


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate deterministic synthetic data for bss-core"
    )
    parser.add_argument(
        "--seed", type=int, default=20261108,
        help="Deterministic seed (default: 20261108)",
    )
    parser.add_argument(
        "--out", type=str, default="docs/prototype/generator/output",
        help="Output directory (default: docs/prototype/generator/output)",
    )
    args = parser.parse_args()

    counts = generate_synthetic_data(seed=args.seed, out_dir=args.out)
    print(f"\nDone. Seed: {args.seed}")
    for name, count in counts.items():
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()