"""User administration Streamlit page for bss-core Support Application."""

import streamlit as st
from typing import Optional, List

from application.use_cases.users import (
    create_user,
    update_user_role,
    update_user_status,
    search_users,
    toggle_user_status,
    get_user_permissions,
)
from domain.entities import User, UserRole, UserStatus


st.set_page_config(page_title="User Administration", page_icon="👥")

st.title("👥 User Administration")

st.markdown("---")

st.header("Create User")

with st.form("user_create_form", clear_on_submit=True):
    name = st.text_input("Name *", placeholder="e.g., John Doe")
    email = st.text_input("Email *", placeholder="e.g., john@example.com")
    role = st.selectbox("Role", [r.value for r in UserRole])
    status = st.selectbox("Status", [s.value for s in UserStatus])
    
    submitted = st.form_submit_button("Create User")

    if submitted:
        if not name.strip():
            st.error("Name is required")
        elif not email.strip() or "@" not in email:
            st.error("Valid email is required")
        else:
            try:
                user = create_user(
                    name=name.strip(),
                    email=email.strip(),
                    role=UserRole(role),
                    status=UserStatus(status),
                )
                st.success(f"User created: {user.name} ({user.email}) - Role: {user.role}")
            except ValueError as e:
                st.error(f"Error: {e}")

st.markdown("---")

st.header("User List")

with st.expander("Search users"):
    name_filter = st.text_input("Name filter (optional)")
    email_filter = st.text_input("Email filter (optional)")
    role_filter = st.selectbox("Role filter", [None] + [r.value for r in UserRole])

if st.button("Search Users"):
    try:
        users = search_users(
            name_filter=name_filter.strip() if name_filter else None,
            email_filter=email_filter.strip() if email_filter else None,
            role_filter=UserRole(role_filter) if role_filter else None,
        )
        
        if users:
            st.write(f"Found {len(users)} users:")
            for u in users:
                with st.expander(f"{u.name} - {u.email}"):
                    st.write(f"**ID:** {u.id}")
                    st.write(f"**Role:** {u.role}")
                    st.write(f"**Status:** {u.status}")
        else:
            st.info("No users found")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

st.header("User Management")

user_id = st.text_input("Enter user ID to manage")
if user_id:
    st.write(f"User: {user_id}")
    
    st.write("### Update Role")
    with st.form("user_role_form"):
        new_role = st.selectbox("New role", [r.value for r in UserRole])
        role_submitted = st.form_submit_button("Update Role")
        
        if role_submitted:
            try:
                # Create a user object and update role
                from domain.entities import User
                user = User(id=user_id)
                user = update_user_role(user, UserRole(new_role))
                st.success(f"Role updated to: {user.role}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.write("### Toggle Status")
    with st.form("user_status_form"):
        toggle_submitted = st.form_submit_button("Toggle Status")
        
        if toggle_submitted:
            try:
                from domain.entities import User
                user = User(id=user_id)
                user = toggle_user_status(user)
                st.success(f"Status toggled to: {user.status}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.write("### View Permissions")
    if st.button("Show Permissions"):
        try:
            from domain.entities import User
            user = User(id=user_id)
            permissions = get_user_permissions(user)
            st.write(f"Permissions: {permissions}")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

st.header("Audit Context")

st.write("Per AD-5: User-management mutations are audit-logged.")
st.info("All user CRUD operations produce audit entries in the append-only audit log.")