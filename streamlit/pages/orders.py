"""Orders and returns Streamlit page for bss-core Support Application."""

import streamlit as st
from decimal import Decimal
from typing import Optional, List

from application.use_cases.orders import create_order, add_order_item, remove_order_item, transition_order_status, check_return_eligibility
from application.use_cases.order_status import transition_to_processing, transition_to_completed, transition_to_returned, transition_to_cancelled, can_transition_to
from application.use_cases.returns import create_return_request, submit_return, process_idempotent_return
from application.use_cases.return_eligibility import evaluate_return_eligibility, can_submit_return
from domain.entities import Order, OrderStatus, ReturnStatus, OrderItem


st.set_page_config(page_title="Orders & Returns", page_icon="🛒")

st.title("🛒 Orders and Returns")

st.markdown("---")

st.header("Create Order")

with st.form("order_create_form", clear_on_submit=True):
    customer_id = st.text_input("Customer ID *", placeholder="e.g., cust_001")
    with st.expander("Add order items"):
        product_id = st.text_input("Product ID *", placeholder="e.g., prod_001")
        quantity = st.number_input("Quantity *", min_value=1, value=1)
        unit_price = st.number_input("Unit Price *", min_value=0.01, value=10.00)
    
    submitted = st.form_submit_button("Create Order")

    if submitted:
        if not customer_id.strip():
            st.error("Customer ID is required")
        elif not product_id.strip():
            st.error("Product ID is required")
        else:
            try:
                items = [{"product_id": product_id.strip(), "quantity": quantity, "unit_price": float(unit_price)}]
                order = create_order(customer_id=customer_id.strip(), items=items)
                st.success(f"Order created: {order.id} - Status: {order.status} - Total: ${order.total_amount:.2f}")
            except ValueError as e:
                st.error(f"Error: {e}")

st.markdown("---")

st.header("Order Management")

order_id = st.text_input("Enter order ID to manage")
if order_id:
    st.write(f"Order: {order_id}")
    
    st.write("### Status Transition")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Processing"):
            try:
                order = transition_to_processing(None)  # Placeholder
                st.success(f"Status: {order.status}")
            except Exception as e:
                st.error(f"Error: {e}")
    with col2:
        if st.button("Completed"):
            try:
                order = transition_to_completed(None)  # Placeholder
                st.success(f"Status: {order.status}")
            except Exception as e:
                st.error(f"Error: {e}")
    with col3:
        if st.button("Returned"):
            try:
                order = transition_to_returned(None)  # Placeholder
                st.success(f"Status: {order.status}")
            except Exception as e:
                st.error(f"Error: {e}")
    with col4:
        if st.button("Cancelled"):
            try:
                order = transition_to_cancelled(None)  # Placeholder
                st.success(f"Status: {order.status}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.write("### Return Eligibility")
    if st.button("Check Eligibility"):
        try:
            eligibility = check_return_eligibility(None)  # Placeholder
            st.json(eligibility)
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.write("### Create Return Request")
    with st.form("return_create_form"):
        reason = st.text_area("Return reason *", placeholder="e.g., Item defective")
        rq_quantity = st.number_input("Quantity to return *", min_value=1, value=1)
        rq_idempotency = st.text_input("Idempotency Key *", placeholder="e.g., key-123")
        rq_submitted = st.form_submit_button("Submit Return")
        
        if rq_submitted:
            if not reason.strip():
                st.error("Reason is required")
            elif not rq_idempotency.strip():
                st.error("Idempotency key is required")
            else:
                try:
                    return_request = submit_return(
                        order_item_id=order_id,
                        idempotency_key=rq_idempotency.strip(),
                        reason=reason.strip(),
                        quantity=rq_quantity,
                    )
                    st.success(f"Return submitted: {return_request.rma_number}")
                    st.info(f"Shipping label: {return_request.shipping_label_url}")
                except ValueError as e:
                    st.error(f"Error: {e}")

st.markdown("---")

st.header("Return Status")

return_id = st.text_input("Enter return ID to view status")
if return_id:
    try:
        return_request = process_idempotent_return(return_id)
        if return_request:
            st.json({
                "id": str(return_request.id),
                "rma_number": return_request.rma_number,
                "status": return_request.status,
                "shipping_label": return_request.shipping_label_url,
            })
        else:
            st.info("Return not found")
    except Exception as e:
        st.error(f"Error: {e}")