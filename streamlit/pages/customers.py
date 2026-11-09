"""Customer management Streamlit page for bss-core Support Application."""

import streamlit as st
from typing import Optional


def show() -> None:

    from application.use_cases.customers import create_customer, update_customer_tier, list_customers, get_customer_profile
    from api.routes.customers import create_customer_route, list_customers_route, get_customer_profile as get_profile_route

    st.title("👤 Customer Management")

    st.markdown("---")

    st.header("Create Customer")

    with st.form("customer_create_form", clear_on_submit=True):
        name = st.text_input("Name *", placeholder="e.g., Acme Corp")
        email = st.text_input("Email *", placeholder="e.g., contact@acme.com")
        tier = st.selectbox("Tier", ["Standard", "Gold", "Enterprise"])
        submitted = st.form_submit_button("Create Customer")

        if submitted:
            if not name.strip():
                st.error("Name is required")
            elif not email.strip() or "@" not in email:
                st.error("Valid email is required")
            else:
                try:
                    customer = create_customer(name=name.strip(), email=email.strip(), tier=tier)
                    st.success(f"Customer created: {customer.name} ({customer.email}) - Tier: {customer.tier}")
                except ValueError as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    st.header("Customer List")

    tier_filter = st.selectbox("Filter by tier", [None, "Standard", "Gold", "Enterprise"])
    customers = list_customers(tier=tier_filter)

    if customers:
        for c in customers:
            with st.expander(f"{c.name} - {c.email}"):
                st.write(f"**ID:** {c.id}")
                st.write(f"**Tier:** {c.tier}")
    else:
        st.info("No customers found")

    st.markdown("---")

    st.header("Customer Profile")

    customer_id = st.text_input("Enter customer ID to view profile")
    if customer_id:
        profile = get_customer_profile(None)  # Placeholder
        if profile:
            st.json(profile)
        else:
            st.info("Profile not found")


if __name__ == "__main__":
    show()