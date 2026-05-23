"""Hotels — step-based Search → Results → Payment → Confirmation."""
from datetime import date

import streamlit as st

import api_client
from layout import apply_theme, init_session, render_footer, render_navbar, require_login
from ui_hero_banner import render_search_hero
from ui_components import (
    render_breadcrumb,
    render_hotel_card,
    render_hotel_checkout_gallery,
    render_step_bar,
    set_status,
)
from ui_payment import render_order_summary, render_premium_payment
from ui_hotel_prefs import render_hotel_preferences
from ui_traveller import render_traveller_form, validate_traveller
from user_store import get_profile, get_token

st.set_page_config(page_title="Hotels | TripWise", page_icon="🏨", layout="wide")
init_session()
require_login()
apply_theme()
render_navbar()
render_breadcrumb(["Home", "Hotels"])

if "hotel_step" not in st.session_state:
    st.session_state.hotel_step = "search"

profile = get_profile()
token = get_token()
step = st.session_state.hotel_step
render_step_bar("hotel_step")

if step == "search":
    render_search_hero("hotel")
    city = st.text_input("City", st.session_state.get("prefill_hotel_city", "Dubai"))
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        checkin = st.date_input("Check-in", min_value=date.today(), key="ht_checkin")
    with c2:
        checkout = st.date_input("Check-out", min_value=date.today(), key="ht_checkout")
    with c3:
        rooms = st.number_input("Rooms", 1, 5, 1)
    with c4:
        guests = st.number_input("Guests", 1, 10, 2)
    st.session_state._hotel_dates = (checkin, checkout)
    if st.button("Search Hotels", type="primary", use_container_width=True):
        with st.spinner("Searching..."):
            res = api_client.post_hotel_search(city, rooms=rooms, guests=guests)
            st.session_state.hotel_results = res.get("hotels", [])
            st.session_state.hotel_step = "results"
            set_status(f"Found {len(st.session_state.hotel_results)} hotels in {city}.", "success")
            st.rerun()

elif step == "results":
    hotels = st.session_state.get("hotel_results", [])
    if not hotels:
        st.warning("No results yet.")
        if st.button("Back to Search"):
            st.session_state.hotel_step = "search"
            st.rerun()
    else:
        best = min(hotels, key=lambda h: h["price_night"])
        for h in hotels:
            render_hotel_card(h, is_best=(h["id"] == best["id"]))
            if st.button(f"Book {h['name']}", key=f"book_{h['id']}", type="primary"):
                st.session_state.checkout_hotel = h
                st.session_state.hotel_step = "checkout"
                set_status(f"Selected {h['name']} — review and pay.", "success")
                st.rerun()
        if st.button("New search"):
            st.session_state.hotel_step = "search"
            st.rerun()

elif step == "checkout":
    h = st.session_state.get("checkout_hotel")
    if not h:
        st.warning("No hotel selected.")
        if st.button("View results"):
            st.session_state.hotel_step = "results"
            st.rerun()
    else:
        checkin, checkout = st.session_state.get("_hotel_dates", (date.today(), date.today()))
        nights = max(1, (checkout - checkin).days) if checkout > checkin else 1
        st.markdown('<div class="tw-checkout-page">', unsafe_allow_html=True)
        render_hotel_checkout_gallery(h)
        st.markdown(f"**{h['name']}** · {nights} night(s) · ★ {h.get('rating')}/5 · from Rs {h['price_night']:,}/night")
        st.caption(h.get("cancellation_policy", ""))
        amount = h["price_night"] * nights
        traveller: dict = {}
        pay: dict = {}
        room_prefs: dict = {}
        details_col, pay_col = st.columns([1.55, 1], gap="large")
        with details_col:
            st.markdown("#### Guest & room", unsafe_allow_html=True)
            room_prefs = render_hotel_preferences("ht", base_price_night=h["price_night"], nights=nights)
            amount = room_prefs.get("estimated_total_inr", amount)
            traveller = render_traveller_form(profile, "ht", require_gender=False)
        with pay_col:
            st.markdown('<div class="tw-checkout-pay-sticky">', unsafe_allow_html=True)
            st.markdown("#### Payment", unsafe_allow_html=True)
            pay = render_premium_payment(profile, amount, "hotel", st.session_state.get("user_id"), token)
            summary = room_prefs.get("price_lines") or [("Room total", f"Rs {amount:,}")]
            summary.append(("Insurance", f"Rs 499" if pay["insurance"] else "Rs 0"))
            render_order_summary(summary, pay["total_inr"])
            confirm_h = st.button("Pay & Confirm Hotel", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if confirm_h:
            err = validate_traveller(traveller)
            if err:
                st.error(err)
            else:
                with st.spinner("Processing secure payment..."):
                    booking = api_client.post_hotel_book(
                        h,
                        traveller,
                        nights=nights,
                        coupon=pay["coupon"],
                        insurance=pay["insurance"],
                        payment_method=pay["method_label"],
                        booking_for=traveller.get("booking_for"),
                        room_prefs=room_prefs,
                        room_total_inr=amount,
                        gender=traveller.get("gender", ""),
                        token=token,
                    )
                    api_client.charge_payment(booking["booking_id"], pay["method_id"], pay["total_inr"], token)
                st.session_state.last_hotel_booking = booking
                st.session_state.checkout_hotel = None
                st.session_state.hotel_step = "done"
                who = "yourself" if traveller.get("booking_for") == "self" else traveller.get("full_name")
                set_status(f"Hotel booked for {who}! ID {booking.get('booking_id')}", "success")
                st.balloons()
                st.rerun()
        if st.button("Change hotel"):
            st.session_state.hotel_step = "results"
            st.rerun()

elif step == "done":
    b = st.session_state.get("last_hotel_booking")
    if b:
        st.success(f"Hotel booked! **{b['booking_id']}** · Rs {b.get('amount_inr', 0):,}")
        if st.button("My Trips", type="primary"):
            st.switch_page("pages/5_My_Trips.py")
        if st.button("Book another hotel"):
            st.session_state.hotel_step = "search"
            st.rerun()
    else:
        st.info("Complete payment to see confirmation.")

render_footer()
