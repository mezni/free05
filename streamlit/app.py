"""Streamlit application entry point for bss-core Support Application (MVP)."""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="bss-core Support Application",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.sidebar.title("bss-core MVP")
st.sidebar.markdown("---")

# Navigation setup
page = st.sidebar.radio(
    "Navigation",
    ["Customers", "Orders", "Billing", "Shipments", "Users"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("bss-core Support Application (MVP)")
st.sidebar.caption("Built with FastAPI + Streamlit")

# Route to the selected page
if page == "Customers":
    from streamlit.pages.customers import show
    show()
elif page == "Orders":
    from streamlit.pages.orders import show
    show()
elif page == "Billing":
    from streamlit.pages.billing import show
    show()
elif page == "Shipments":
    from streamlit.pages.shipments import show
    show()
elif page == "Users":
    from streamlit.pages.users import show
    show()