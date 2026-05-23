"""Shared layout: theme, auth gate, sidebar, navbar, footer."""
from pathlib import Path

import streamlit as st

import api_client
from styles import get_animations, get_css
from ui_components import render_status
from user_store import get_mobile, get_profile, is_auth_pending, is_logged_in, logout, restore_session_from_file

ASSETS = Path(__file__).parent / "assets"

NAV_PAGES = [
    ("Home", "pages/1_Home.py"),
    ("Flights", "pages/2_Flights.py"),
    ("Hotels", "pages/3_Hotels.py"),
    ("Support", "pages/4_Support.py"),
    ("Trips", "pages/5_My_Trips.py"),
    ("Refunds", "pages/6_Refunds.py"),
    ("Agents", "pages/7_Agents.py"),
]


def init_session():
    defaults = {
        "theme": "light",
        "messages": [],
        "last_result": None,
        "booking_id": "TW-2026-78421",
        "compare_flights": [],
        "flight_results": [],
        "hotel_results": [],
        "flight_step": "search",
        "hotel_step": "search",
        "checkout_flight": None,
        "checkout_hotel": None,
        "cancel_preview": None,
        "api_connected": None,
        "status_message": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    restore_session_from_file()


def get_api_status() -> tuple[bool, str]:
    if st.session_state.get("api_connected") is None:
        st.session_state.api_connected = api_client.check_api_health()
    if st.session_state.api_connected:
        return True, "Backend Connected"
    return False, "Demo Mode"


def apply_theme():
    """Inject TripWise CSS into the main app (must use st.markdown, not iframe script)."""
    theme = st.session_state.get("theme", "light")
    path = Path(__file__).parent / "animations.css"
    anim = f"<style>{path.read_text(encoding='utf-8')}</style>" if path.exists() else get_animations(theme)
    st.markdown(get_css(theme) + anim, unsafe_allow_html=True)
    st.markdown(
        f'<div class="tw-app-theme tw-app-theme-{theme}" data-theme="{theme}" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )


def require_login():
    init_session()
    if is_logged_in():
        return
    if is_auth_pending():
        st.warning("Complete your profile on the Login page to continue.")
        if st.button("Go to Login", type="primary"):
            st.switch_page("pages/0_Login.py")
        st.stop()
    st.switch_page("pages/0_Login.py")


require_profile = require_login


def render_sidebar():
    """Branded sidebar content (works with Streamlit native page nav)."""
    connected, status_label = get_api_status()
    api_cls = "tw-api-live" if connected else "tw-api-demo"
    with st.sidebar:
        st.markdown(
            '<div class="tw-sidebar-brand">'
            '<div class="tw-sidebar-logo-text">TripWise</div>'
            '<div class="tw-sidebar-tagline">Smart travel booking</div>'
            f'<span class="{api_cls} tw-sidebar-pill">{status_label}</span>'
            "</div>",
            unsafe_allow_html=True,
        )
        if is_logged_in():
            p = get_profile()
            st.markdown(
                f'<div class="tw-sidebar-user">'
                f'<strong>{p.get("full_name", "Guest")}</strong><br/>'
                f'<span>{p.get("mobile", "")}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            st.caption("Sign in via Login to book and save trips.")
        st.caption("Use the top bar for quick navigation.")


def render_navbar():
    render_sidebar()
    connected, status_label = get_api_status()
    api_cls = "tw-api-live" if connected else "tw-api-demo"

    st.markdown(
        f'<div class="tw-topnav-wrap">'
        f'<span class="tw-logo-nav">✈ TripWise</span>'
        f'<span class="{api_cls} tw-topnav-pill">{status_label}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )
    render_status()

    st.markdown('<div class="tw-nav-strip">', unsafe_allow_html=True)
    link_cols = st.columns(7)
    for col, (label, page) in zip(link_cols, NAV_PAGES):
        with col:
            st.page_link(page, label=label, use_container_width=True)

    action_cols = st.columns([3, 1, 1, 1, 1])
    with action_cols[1]:
        if st.button("Light", key="nav_light", use_container_width=True):
            st.session_state.theme = "light"
            st.rerun()
    with action_cols[2]:
        if st.button("Dark", key="nav_dark", use_container_width=True):
            st.session_state.theme = "dark"
            st.rerun()
    with action_cols[3]:
        if st.button("Profile", key="nav_profile_top", use_container_width=True):
            st.session_state.edit_profile = True
            st.switch_page("pages/0_Login.py")
    with action_cols[4]:
        if st.button("Logout", key="nav_logout_top", use_container_width=True):
            logout()
            st.switch_page("pages/0_Login.py")
    st.markdown("</div>", unsafe_allow_html=True)

    _render_notifications()


def _render_notifications():
    if not is_logged_in():
        return
    bookings = api_client.get_my_bookings(st.session_state.get("auth_token"), get_mobile())
    alerts = []
    for b in bookings:
        f = b.get("flight", {})
        status = b.get("flight_status") or f.get("flight_status")
        if b.get("type") == "flight" and status == "Delayed":
            alerts.append(f"Delay: {f.get('airline', '')} {f.get('flight_no', '')}")
        if b.get("status") == "Cancelled":
            alerts.append(f"Cancelled: {b.get('booking_id')}")
    with st.expander(f"Alerts ({len(alerts)})", expanded=False):
        if alerts:
            for a in alerts:
                st.caption(a)
        else:
            st.caption("No active disruption alerts")


def render_footer():
    connected, label = get_api_status()
    st.divider()
    st.caption(
        f"TripWise Capstone · Person 1 Frontend · {label} · "
        f"Logged in: {get_profile().get('mobile', '')} · See INTEGRATION.md for Person 2"
    )
