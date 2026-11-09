"""Streamlit application entry point for bss-core Support Application (MVP).

Provides sidebar navigation between all 5 user story pages.
"""

import sys
import os
from pathlib import Path

# Ensure the streamlit/ directory is on the path for page imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="bss-core Support Application",
    page_icon="🏦",
    layout="wide",
)

# Sidebar navigation
st.sidebar.title("bss-core MVP")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Customers", "Orders", "Billing", "Shipments", "Users"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("bss-core Support Application (MVP) · 2026-11-08")

# Route to the selected page
if page == "Customers":
    from pages.customers import show  # noqa: E501, S405
    show()
elif page == "Orders":
    from pages.orders import show  # noqa: E501, S405
    show()
elif page == "Billing":
    from pages.billing import show  # noqa: E501, S405
    show()
elif page == "Shipments":
    from pages.shipments import show  # noqa: E501, S405
    show()
elif page == "Users":
    from pages.users import show  # noqa: E501, S405
    show()