"""MakeMyTrip-style home hub — cinema hero, bold branding, quick search."""
import streamlit as st

from config import CITIES, TAGLINE
from layout import apply_theme, get_api_status, init_session, render_footer, render_navbar, require_profile
from mock_inventory import OFFERS, TRENDING

HERO_BG = "https://images.unsplash.com/photo-1436491865332-7a61a1099cac?w=1400&q=85"

st.set_page_config(page_title="TripWise Home", page_icon="✈", layout="wide")
init_session()
require_profile()
apply_theme()
render_navbar()

connected, status_label = get_api_status()
pill_cls = "tw-api-live" if connected else "tw-api-demo"

st.markdown(
    f'<div class="tw-hero-cinema tw-animate-in" style="background-image:url({HERO_BG})">'
    f'<span class="tw-hero-cloud" style="top:12%;left:5%">☁</span>'
    f'<span class="tw-hero-cloud" style="top:8%;left:40%;animation-delay:4s">☁</span>'
    f'<span class="tw-hero-plane tw-plane-colored">✈</span>'
    f'<div class="tw-hero-cinema-overlay">'
    f'<h1 class="tw-brand-mega">TripWise</h1>'
    f'<div class="tw-tagline">{TAGLINE}</div>'
    f'<span class="{pill_cls}" style="display:inline-block;margin-top:0.75rem;padding:0.35rem 0.9rem;'
    f'border-radius:999px;background:rgba(255,255,255,0.25);font-weight:700">{status_label}</span>'
    f'<div class="tw-glass-card">'
    f'<b>20+ AI Agents</b> · Instant Refunds · Live Flight Status · Secure Payments'
    f"</div></div></div>",
    unsafe_allow_html=True,
)

if st.session_state.get("show_disruption"):
    st.warning("Disruption: Flight EK-513 DEL→DXB delayed — open AI Support for rebooking options.")

st.markdown("#### Quick book")
tab_f, tab_h, tab_p = st.tabs(["Flights", "Hotels", "Packages"])
with tab_f:
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        hf = st.selectbox("From", CITIES, key="home_from")
    with fc2:
        ht = st.selectbox("To", CITIES, index=1, key="home_to")
    with fc3:
        hd = st.date_input("Depart", key="home_depart")
    if st.button("Search Flights", type="primary", use_container_width=True):
        st.session_state.prefill_flight = {"from": hf, "to": ht, "date": str(hd)}
        st.session_state.flight_step = "search"
        st.switch_page("pages/2_Flights.py")
with tab_h:
    hc = st.text_input("City", value="Dubai", key="home_hotel_city")
    if st.button("Search Hotels", type="primary", use_container_width=True):
        st.session_state.prefill_hotel_city = hc
        st.session_state.hotel_step = "search"
        st.switch_page("pages/3_Hotels.py")
with tab_p:
    st.info("Holiday packages — AI helps modify itinerary before departure.")
    if st.button("Ask AI about packages"):
        st.session_state.pending_query = "Help me modify my holiday package itinerary before departure."
        st.switch_page("pages/4_Support.py")

st.markdown("#### Explore destinations")
promo_cols = st.columns(3)
promos = [
    ("Weekend Getaways", "Goa from Rs 4,500", "GOI"),
    ("International", "Dubai from Rs 18,200", "DXB"),
    ("Budget Stays", "Hotels from Rs 2,100/night", "Dubai"),
]
for col, (title, sub, code) in zip(promo_cols, promos):
    with col:
        st.markdown(
            f'<div class="tw-promo-card tw-animate-in"><b>{title}</b><br/><small>{sub}</small></div>',
            unsafe_allow_html=True,
        )
        if st.button(f"Explore {title}", key=f"promo_{title}", use_container_width=True):
            if title == "Budget Stays":
                st.session_state.prefill_hotel_city = "Dubai"
                st.session_state.hotel_step = "search"
                st.switch_page("pages/3_Hotels.py")
            else:
                st.session_state.prefill_flight = {"from": "Delhi (DEL)", "to_code": code}
                st.session_state.flight_step = "search"
                st.switch_page("pages/2_Flights.py")

st.markdown("#### Offers")
offer_cols = st.columns(len(OFFERS))
for col, o in zip(offer_cols, OFFERS):
    with col:
        st.markdown(
            f'<div class="tw-offer-card"><b>{o["code"]}</b><br/><small>{o["title"]}</small></div>',
            unsafe_allow_html=True,
        )

st.markdown("#### Trending")
cols = st.columns(len(TRENDING))
for col, t in zip(cols, TRENDING):
    with col:
        if st.button(f"{t['dest']} from Rs {t['price']:,}", key=f"trend_{t['dest']}", use_container_width=True):
            st.session_state.prefill_flight = {"from": "Delhi (DEL)", "to_code": t["to"]}
            st.session_state.flight_step = "search"
            st.switch_page("pages/2_Flights.py")

render_footer()
