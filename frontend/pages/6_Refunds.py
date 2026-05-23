"""Refund tracker — from bookings."""
import streamlit as st

import api_client
from layout import apply_theme, init_session, render_footer, render_navbar, require_login
from ui_components import render_refund_timeline

st.set_page_config(page_title="Refunds", page_icon="💰", layout="wide")
init_session()
require_login()
apply_theme()
render_navbar()

from user_store import get_mobile

refunds = api_client.get_all_refunds(get_mobile())
bookings = api_client.get_my_bookings(st.session_state.get("auth_token"), get_mobile())
cancelled = [b for b in bookings if b.get("status") == "Cancelled"]

if not refunds and not cancelled:
    st.info("No refunds yet. Cancel a booking from My Trips.")
else:
    booking_map = {b.get("booking_id"): b for b in bookings}
    for r in refunds:
        with st.container(border=True):
            bid = r.get("booking_id")
            b = booking_map.get(bid, {})
            if b.get("type") == "hotel" and b.get("hotel", {}).get("image_url"):
                st.image(b["hotel"]["image_url"], width=280)
            st.markdown(f"**Refund** `{r.get('refund_id')}` · Booking `{bid}`")
            st.metric("Amount", f"Rs {r.get('amount_inr', 0):,}")
            st.write(f"Status: **{r.get('status')}**")
            if r.get("timeline"):
                render_refund_timeline(r["timeline"])
    for b in cancelled:
        if not any(r.get("booking_id") == b.get("booking_id") for r in refunds):
            st.caption(f"Cancelled booking {b.get('booking_id')} — refund processing")

if st.button("Ask AI about refund"):
    st.session_state.pending_query = "Why has my refund not been credited yet?"
    st.switch_page("pages/4_Support.py")

render_footer()
