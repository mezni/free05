"""Shipments and tracking Streamlit page for bss-core Support Application."""


def show() -> None:
    import streamlit as st
    from datetime import datetime, timedelta
    from typing import Optional, List

    from application.use_cases.shipments import (
        create_shipment,
        advance_shipment_status,
        get_shipment_tracking_info,
        calculate_shipment_eta,
    )
    from infrastructure.carriers.mock_adapter import MockCarrierAdapter

    st.title("🚚 Shipments and Tracking")

    st.markdown("---")

    st.header("Create Shipment")

    with st.form("shipment_create_form", clear_on_submit=True):
        order_id = st.text_input("Order ID *", placeholder="e.g., ord_001")
        carrier = st.selectbox("Carrier", ["FedEx", "UPS", "DHL"])
        eta_str = st.text_input("Estimated Delivery Date (YYYY-MM-DD, optional)", placeholder="e.g., 2026-12-20")
        
        submitted = st.form_submit_button("Create Shipment")

        if submitted:
            if not order_id.strip():
                st.error("Order ID is required")
            else:
                try:
                    eta = None
                    if eta_str.strip():
                        eta = datetime.strptime(eta_str.strip(), "%Y-%m-%d").date()

                    shipment = create_shipment(
                        order_id=order_id.strip(),
                        carrier=carrier,
                        estimated_delivery_date=eta,
                    )

                    st.success(f"Shipment created: {shipment.tracking_number}")
                    st.info(f"Carrier: {shipment.carrier}")
                    st.info(f"Status: {shipment.status}")
                    st.info(f"ETA: {shipment.estimated_delivery_date}")
                except ValueError as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    st.header("Shipment Tracking")

    tracking_number = st.text_input("Enter tracking number to view status")
    if tracking_number:
        try:
            shipment_info = {
                "tracking_number": tracking_number,
            }
            info = {
                "tracking_number": tracking_number,
            }
            # Try mock adapter
            adapter_shipment = None
            try:
                from infrastructure.carriers.mock_adapter import MockCarrierAdapter
                adapter = MockCarrierAdapter()
                adapter_shipment = adapter.get_shipment(tracking_number)
            except Exception:
                pass

            if adapter_shipment:
                st.write(f"**Tracking Number:** {adapter_shipment['tracking_number']}")
                st.write(f"**Carrier:** {adapter_shipment['carrier']}")
                st.write(f"**Status:** {adapter_shipment['status']}")
                eta = adapter_shipment.get("estimated_delivery_date")
                if eta:
                    st.write(f"**ETA:** {eta}")
                st.write(f"**Created:** {adapter_shipment.get('created_at')}")

                # Advance status button
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("→ In Transit"):
                        try:
                            result = adapter.advance_status(tracking_number)
                            if result:
                                st.success(f"Status advanced to: {result['status']}")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

                with col2:
                    if st.button("→ Out for Delivery"):
                        try:
                            result = adapter.advance_status(tracking_number)
                            if result:
                                st.success(f"Status advanced to: {result['status']}")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

                with col3:
                    if st.button("→ Delivered"):
                        try:
                            result = adapter.advance_status(tracking_number)
                            if result:
                                st.success(f"Status advanced to: {result['status']}")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            else:
                st.info("Shipment not found in mock adapter. Create a new shipment above.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")

    st.header("Advance Shipment Status")

    with st.form("shipment_advance_form", clear_on_submit=True):
        advance_tracking = st.text_input("Tracking number *", placeholder="e.g., TRK-ABC123")
        with st.expander("Valid status transitions"):
            st.write("Label Created → In Transit")
            st.write("In Transit → Out for Delivery")
            st.write("Out for Delivery → Delivered")
        
        new_status = st.selectbox(
            "New status",
            ["In Transit", "Out for Delivery", "Delivered"],
        )
        
        advance_submitted = st.form_submit_button("Advance Status")

        if advance_submitted:
            if not advance_tracking.strip():
                st.error("Tracking number is required")
            else:
                try:
                    # Advance status in mock adapter
                    from infrastructure.carriers.mock_adapter import MockCarrierAdapter
                    adapter = MockCarrierAdapter()
                    result = adapter.advance_status(advance_tracking.strip())
                    
                    if result:
                        st.success(f"Shipment status advanced to: {result['status']}")
                        st.info(f"Updated at: {result['updated_at']}")
                    else:
                        st.info("No status change needed or shipment not found")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    st.header("Shipment ETA")

    eta_tracking = st.text_input("Enter tracking number for ETA")
    if eta_tracking:
        try:
            from application.use_cases.shipments import calculate_shipment_eta
            # Try mock adapter first
            from infrastructure.carriers.mock_adapter import MockCarrierAdapter
            adapter = MockCarrierAdapter()
            adapter_shipment = adapter.get_shipment(eta_tracking)
            
            if adapter_shipment:
                eta = calculate_shipment_eta_from_dict(adapter_shipment)
                if eta:
                    st.success(f"Estimated Delivery Date: {eta.strftime('%Y-%m-%d')}")
                else:
                    st.info("Could not calculate ETA")
            else:
                st.info("Shipment not found in mock adapter")
        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    show()