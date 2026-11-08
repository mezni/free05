"""Billing and refunds Streamlit page for bss-core Support Application."""

import streamlit as st
from decimal import Decimal
from typing import Optional, List

from application.use_cases.billing import create_billing_record, list_billing_records, mask_payment_method, get_balance, mask_sensitive_data, format_currency_amount
from application.use_cases.refunds import process_refund, process_refund_with_audit_check, calculate_customer_balance
from infrastructure.repositories.audit import audit_repository
from domain.entities import Customer, BillingType, BillingStatus


st.set_page_config(page_title="Billing and Refunds", page_icon="💰")

st.title("💰 Billing and Refunds")

st.markdown("---")

st.header("Create Billing Record")

with st.form("billing_create_form", clear_on_submit=True):
    customer_id = st.text_input("Customer ID *", placeholder="e.g., cust_001")
    order_id = st.text_input("Order ID (optional)", placeholder="e.g., ord_001")
    billing_type = st.selectbox("Billing Type", [t.value for t in BillingType])
    amount = st.number_input("Amount *", min_value=0.01, value=19.99)
    currency = st.text_input("Currency", value="USD")
    reason = st.text_area("Reason *", placeholder="e.g., Purchase of items")
    
    submitted = st.form_submit_button("Create Billing Record")

    if submitted:
        if not customer_id.strip():
            st.error("Customer ID is required")
        elif not amount or amount <= 0:
            st.error("Amount must be greater than 0")
        else:
            try:
                billing_type_enum = BillingType(billing_type)
                customer = Customer(id=customer_id.strip())  # Simplified
                record = create_billing_record(
                    customer=customer,
                    order=None if not order_id.strip() else order_id.strip(),
                    billing_type=billing_type_enum,
                    amount=Decimal(str(amount)),
                    currency=currency,
                )
                st.success(f"Billing record created: {record.id}")
                st.info(f"Amount: ${record.amount:.2f} - Type: {record.type}")
                st.info(f"Payment mask: {record.payment_method_mask}")
            except ValueError as e:
                st.error(f"Error: {e}")

st.markdown("---")

st.header("Billing History")

customer_id = st.text_input("Enter customer ID to view billing history")
if customer_id:
    try:
        customer = Customer(id=customer_id.strip())  # Simplified
        records = list_billing_records(customer_id=customer_id.strip())
        
        if records:
            st.write(f"Found {len(records)} billing records:")
            for r in records:
                with st.expander(f"{r.type} - ${r.amount:.2f}"):
                    st.write(f"**ID:** {r.id}")
                    st.write(f"**Amount:** ${r.amount:.2f} {r.currency}")
                    st.write(f"**Type:** {r.type}")
                    st.write(f"**Status:** {r.status}")
                    st.write(f"**Payment Mask:** {r.payment_method_mask}")
                    st.write(f"**Created:** {r.created_at.isoformat() if r.created_at else 'N/A'}")
        else:
            st.info("No billing records found")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

st.header("Issue Refund")

with st.form("refund_create_form", clear_on_submit=True):
    refund_customer_id = st.text_input("Customer ID *", placeholder="e.g., cust_001")
    refund_amount = st.number_input("Refund Amount *", min_value=0.01, value=19.99)
    refund_reason = st.text_area("Refund Reason *", placeholder="e.g., Customer returned item")
    refund_submitted = st.form_submit_button("Issue Refund")

    if refund_submitted:
        if not refund_customer_id.strip():
            st.error("Customer ID is required")
        elif not refund_amount or refund_amount <= 0:
            st.error("Amount must be greater than 0")
        elif not refund_reason.strip():
            st.error("Reason is required")
        else:
            try:
                customer = Customer(id=refund_customer_id.strip())  # Simplified
                result = process_refund_with_audit_check(
                    customer=customer,
                    amount=Decimal(str(refund_amount)),
                    reason=refund_reason.strip(),
                )
                
                st.success(f"Refund issued: {result['refund_record']['id']}")
                st.info(f"Amount: ${result['refund_record']['amount']}")
                st.info(f"Audit entry created: {result['audit_guarantee']}")
                
                # Show audit entry
                if result['audit_entry']:
                    with st.expander("View Audit Entry"):
                        st.json(result['audit_entry'])
            except ValueError as e:
                st.error(f"Validation error: {e}")
            except RuntimeError as e:
                st.error(f"Refund blocked: {e} (audit failure)")

st.markdown("---")

st.header("Customer Balance")

balance_customer_id = st.text_input("Enter customer ID to check balance")
if balance_customer_id:
    try:
        customer = Customer(id=balance_customer_id.strip())  # Simplified
        balance_info = calculate_customer_balance(customer)
        
        st.success(f"Customer Balance: ${balance_info['balance']} USD")
        
        with st.expander("Details"):
            st.write(f"**Customer ID:** {balance_info['customer_id']}")
            st.write(f"**Currency:** {balance_info['currency']}")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

st.header("Audit Log")

st.write("Append-only audit log entries:")

with st.expander("View audit entries"):
    entries = audit_repository.get_entries()
    if entries:
        for entry in entries[:10]:  # Show last 10
            st.json({
                "id": str(entry.id),
                "actor": entry.actor_user_id,
                "operation": entry.operation,
                "entity": entry.entity_type,
                "entity_id": entry.entity_id,
                "outcome": entry.outcome,
                "amount": str(entry.amount) if entry.amount else None,
                "created_at": entry.created_at.isoformat() if entry.created_at else None,
            })
    else:
        st.info("No audit entries found")