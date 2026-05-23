"""My bookings — cancel, refund preview, flight status."""
import streamlit as st

import api_client
import mock_demo
from layout import apply_theme, init_session, render_footer, render_navbar, require_login
from ui_components import set_status
from ui_components import render_flight_status, render_hotel_card, render_refund_timeline
from user_store import get_mobile, get_token

st.set_page_config(page_title="My Trips", page_icon="📋", layout="wide")
init_session()
require_login()
apply_theme()
render_navbar()

token = get_token()
mobile = get_mobile()
bookings = api_client.get_my_bookings(token, mobile)

if not bookings:
    st.info("No trips yet. Book a flight or hotel from the menu.")
else:
    for b in reversed(bookings):
        with st.container(border=True):
            if b.get("type") == "flight":
                f = b.get("flight", {})
                st.markdown(f"**Flight** `{b.get('booking_id')}` · PNR **{b.get('pnr')}** · Rs {b.get('amount_inr', 0):,}")
                st.write(f"{f.get('airline')} {f.get('flight_no')} · {b.get('status')}")
                if b.get("seats"):
                    st.caption(f"Seats: {', '.join(b['seats'])} · {b.get('seat_position', '').title()} · {b.get('seat_zone', '').title()} zone")
                elif b.get("seat"):
                    st.caption(f"Seat {b['seat']} · {b.get('gender', '')}")
                if b.get("gender") and not b.get("seat"):
                    st.caption(f"Gender: {b['gender']}")
                render_flight_status(f)
                if b.get("status") != "Cancelled":
                    if st.button("Cancel / Refund", key=f"cx_{b['booking_id']}"):
                        prev = api_client.cancel_preview(b["booking_id"], token)
                        st.session_state.cancel_preview = prev
                        st.session_state.cancel_bid = b["booking_id"]
            else:
                h = b.get("hotel", {})
                render_hotel_card(h, show_image=True)
                st.markdown(f"**Hotel** `{b.get('booking_id')}` · Rs {b.get('amount_inr', 0):,}")
                prefs = b.get("room_prefs") or {}
                if prefs:
                    st.caption(
                        f"{prefs.get('room_type', '')} · {prefs.get('bed', '')} bed · "
                        f"{prefs.get('guests', '')} guests · {prefs.get('smoking', '')}"
                    )
                if b.get("status") != "Cancelled":
                    if st.button("Cancel hotel", key=f"cxh_{b['booking_id']}"):
                        prev = api_client.cancel_preview(b["booking_id"], token)
                        st.session_state.cancel_preview = prev
                        st.session_state.cancel_bid = b["booking_id"]
            if b.get("type") == "flight" and b.get("status") == "Confirmed":
                if st.button("Simulate delay", key=f"delay_{b['booking_id']}"):
                    mock_demo.demo_simulate_delay(b["booking_id"])
                    st.rerun()

if st.session_state.get("cancel_preview"):
    prev = st.session_state.cancel_preview
    st.divider()
    st.markdown("### Cancellation preview")
    st.write(prev.get("policy_text", ""))
    st.metric("Estimated refund", f"Rs {prev.get('refund_eligible_inr', 0):,}")
    st.metric("Fee", f"Rs {prev.get('cancellation_fee_inr', 0):,}")
    if prev.get("timeline"):
        render_refund_timeline(prev["timeline"])
    if st.button("Confirm cancellation", type="primary"):
        api_client.cancel_booking(st.session_state.cancel_bid, token)
        st.session_state.cancel_preview = None
        set_status("Booking cancelled. Track refund on the Refunds page.", "success")
        st.rerun()

render_footer()
