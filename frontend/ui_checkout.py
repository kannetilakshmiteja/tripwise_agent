"""Checkout layout helpers — flight / hotel booking summary."""
import html

import streamlit as st


def render_flight_checkout_banner(flight: dict, pax: int, travel_class: str, base_fare: int) -> None:
    st.markdown(
        '<div class="tw-flight-checkout-banner">'
        f'<div class="tw-flight-checkout-route">'
        f'<span class="tw-flight-checkout-icon">✈</span>'
        f'<div><strong>{html.escape(flight.get("airline", ""))} {html.escape(flight.get("flight_no", ""))}</strong>'
        f'<div class="tw-flight-checkout-meta">'
        f'{html.escape(str(flight.get("from", "")))} → {html.escape(str(flight.get("to", "")))}'
        f' · {html.escape(travel_class)} · {pax} passenger(s)'
        f"</div></div></div>"
        f'<div class="tw-flight-checkout-fare">From <strong>Rs {base_fare:,}</strong></div>'
        "</div>",
        unsafe_allow_html=True,
    )
