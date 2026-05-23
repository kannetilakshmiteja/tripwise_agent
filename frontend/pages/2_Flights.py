"""Flights — step-based Search → Results → Payment → Confirmation."""
from datetime import date

import streamlit as st

import api_client
from config import CITIES, CITY_CODES
from layout import apply_theme, init_session, render_footer, render_navbar, require_login
from ui_hero_banner import render_search_hero
from ui_components import (
    render_breadcrumb,
    render_flight_card,
    render_flight_status,
    render_step_bar,
    set_status,
)
from ui_checkout import render_flight_checkout_banner
from ui_payment import render_order_summary, render_premium_payment
from ui_seat_map import render_checkout_substeps, render_seat_map, validate_seat_selection
from ui_traveller import render_traveller_form, validate_traveller
from user_store import get_profile, get_token

st.set_page_config(page_title="Flights | TripWise", page_icon="✈", layout="wide")
init_session()
require_login()
apply_theme()
render_navbar()
render_breadcrumb(["Home", "Flights"])

if "flight_step" not in st.session_state:
    st.session_state.flight_step = "search"

profile = get_profile()
token = get_token()
step = st.session_state.flight_step
render_step_bar("flight_step")

if step == "search":
    render_search_hero("flight")
    prefill = st.session_state.get("prefill_flight", {})
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        from_city = st.selectbox("From", CITIES, index=CITIES.index(prefill["from"]) if prefill.get("from") in CITIES else 0)
    with c2:
        to_city = st.selectbox("To", CITIES, index=1)
    with c3:
        st.date_input("Depart", min_value=date.today(), key="fl_depart")
    with c4:
        adults = st.number_input("Adults", 1, 9, 1)
        children = st.number_input("Children", 0, 6, 0)
    with c5:
        travel_class = st.selectbox("Class", ["Economy", "Business"])
    passengers = adults + children
    st.session_state.flight_travel_class = travel_class
    from_code = CITY_CODES.get(from_city, "DEL")
    to_code = prefill.get("to_code") or CITY_CODES.get(to_city, "DXB")
    st.info("Cheapest day this week: Tuesday — save up to Rs 2,400")
    if st.button("Search Flights", type="primary", use_container_width=True):
        with st.spinner("Searching..."):
            st.session_state.flight_passengers = passengers
            res = api_client.post_flight_search(from_code, to_code, passengers=passengers, travel_class=travel_class)
            st.session_state.flight_results = res.get("flights", [])
            st.session_state.flight_step = "results"
            set_status(f"Found {len(st.session_state.flight_results)} flights — lowest fare first.", "success")
            st.rerun()
    if st.button("AI: Find lowest fare"):
        st.session_state.pending_query = f"Find cheapest flight {from_code} to {to_code}"
        st.switch_page("pages/4_Support.py")

elif step == "results":
    flights = st.session_state.get("flight_results", [])
    if not flights:
        st.warning("No results yet. Go back to Search.")
        if st.button("Back to Search"):
            st.session_state.flight_step = "search"
            st.rerun()
    else:
        lowest = flights[0]["price_inr"]
        for f in flights:
            c1, c2 = st.columns([3, 1])
            with c1:
                render_flight_card(f, is_lowest=(f["price_inr"] == lowest))
                render_flight_status(f)
            with c2:
                if st.button("Select", key=f"sel_{f['id']}", type="primary", use_container_width=True):
                    st.session_state.checkout_flight = f
                    st.session_state.flight_step = "checkout"
                    set_status(f"Selected {f['airline']} {f['flight_no']} — proceed to payment.", "success")
                    st.rerun()
        if st.button("New search"):
            st.session_state.flight_step = "search"
            st.rerun()

elif step == "checkout":
    f = st.session_state.get("checkout_flight")
    if not f:
        st.warning("No flight selected.")
        if st.button("View results"):
            st.session_state.flight_step = "results"
            st.rerun()
    else:
        pax = st.session_state.get("flight_passengers", 1)
        travel_class = st.session_state.get("flight_travel_class", "Economy")
        base_fare = f.get("price_inr", 0) * pax
        flight_id = str(f.get("id", "x"))
        st.markdown('<div class="tw-checkout-page">', unsafe_allow_html=True)
        render_flight_checkout_banner(f, pax, travel_class, base_fare)
        render_flight_status(f)
        render_checkout_substeps("seat")
        seat_fees = 0
        seat_info: dict = {}
        traveller: dict = {}
        pay: dict = {}
        subtotal = base_fare
        details_col, pay_col = st.columns([1.55, 1], gap="large")
        with details_col:
            st.markdown("#### Traveller details", unsafe_allow_html=True)
            traveller = render_traveller_form(profile, "fl", require_gender=True)
            st.markdown("#### Select seat", unsafe_allow_html=True)
            seat_info = render_seat_map(pax, travel_class, key_prefix=f"fl_{flight_id}", flight_id=flight_id)
            seat_fees = seat_info.get("seat_fees_inr", 0)
            subtotal = base_fare + seat_fees
        with pay_col:
            st.markdown('<div class="tw-checkout-pay-sticky">', unsafe_allow_html=True)
            st.markdown("#### Payment", unsafe_allow_html=True)
            pay = render_premium_payment(profile, subtotal, "flight", st.session_state.get("user_id"), token)
            summary_lines = [("Base fare", f"Rs {base_fare:,}")]
            for line in seat_info.get("seat_fee_breakdown", []):
                summary_lines.append(("Seat surcharge", line))
            if seat_fees and not seat_info.get("seat_fee_breakdown"):
                summary_lines.append(("Seat surcharges", f"Rs {seat_fees:,}"))
            summary_lines.append(("Insurance", f"Rs 499" if pay["insurance"] else "Rs 0"))
            render_order_summary(summary_lines, pay["total_inr"])
            confirm = st.button("Pay & Confirm Booking", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if confirm:
            err = validate_traveller(traveller, require_gender=True)
            if err:
                st.error(err)
            else:
                seat_err = validate_seat_selection(seat_info.get("seats", []), pax, flight_id)
                if seat_err:
                    st.error(seat_err)
                else:
                    with st.spinner("Processing secure payment..."):
                        booking = api_client.post_flight_book(
                            {**f, "price_total": subtotal},
                            traveller,
                            coupon=pay["coupon"],
                            insurance=pay["insurance"],
                            payment_method=pay["method_label"],
                            booking_for=traveller.get("booking_for"),
                            seat=seat_info.get("seat", ""),
                            seats=seat_info.get("seats", []),
                            seat_position=seat_info.get("seat_position", ""),
                            seat_zone=seat_info.get("seat_zone", ""),
                            seat_fees_inr=seat_fees,
                            gender=traveller.get("gender", ""),
                            token=token,
                        )
                        if booking.get("error"):
                            st.error(booking["error"])
                            st.stop()
                        api_client.charge_payment(booking["booking_id"], pay["method_id"], pay["total_inr"], token)
                    st.session_state.last_booking = booking
                    st.session_state.checkout_flight = None
                    st.session_state.flight_step = "done"
                    who = "yourself" if traveller.get("booking_for") == "self" else traveller.get("full_name")
                    seats_txt = ", ".join(seat_info.get("seats", []))
                    set_status(f"Flight booked for {who}! PNR {booking.get('pnr')} · Seats {seats_txt}", "success")
                    st.balloons()
                    st.rerun()
        if st.button("Change flight"):
            st.session_state.flight_step = "results"
            st.rerun()

elif step == "done":
    b = st.session_state.get("last_booking")
    if b:
        render_search_hero("flight")
        seat_line = ""
        if b.get("seats"):
            seat_line = f" · Seats **{', '.join(b['seats'])}**"
        elif b.get("seat"):
            seat_line = f" · Seat **{b['seat']}**"
        st.success(
            f"Booked! PNR **{b.get('pnr')}** · ID **{b.get('booking_id')}** · Rs {b.get('amount_inr', 0):,}{seat_line}"
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("View My Trips", type="primary", use_container_width=True):
                st.switch_page("pages/5_My_Trips.py")
        with c2:
            if st.button("Book another flight", use_container_width=True):
                st.session_state.flight_step = "search"
                st.session_state.flight_results = []
                st.rerun()
    else:
        st.info("Complete payment to see confirmation.")
        if st.button("Go to search"):
            st.session_state.flight_step = "search"
            st.rerun()

render_footer()
