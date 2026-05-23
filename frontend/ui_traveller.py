"""Traveller details at checkout — self or someone else (MakeMyTrip-style)."""
import re

import streamlit as st

GENDER_OPTIONS = ["Male", "Female", "Other", "Prefer not to say"]


def render_traveller_form(profile: dict, key_prefix: str = "tr", require_gender: bool = False) -> dict:
    """Returns traveller dict from form fields (validate with validate_traveller before book)."""
    st.markdown('<div class="tw-traveller-panel"><div class="tw-form-title">Traveller details</div>', unsafe_allow_html=True)
    who = st.radio(
        "Who is travelling?",
        ["Myself", "Someone else"],
        horizontal=True,
        key=f"{key_prefix}_who",
    )
    is_self = who == "Myself"
    if is_self:
        st.caption("Using your account profile. Edit below if booking for yourself with different contact.")
        name = st.text_input("Full name *", value=profile.get("full_name", ""), key=f"{key_prefix}_name")
        email = st.text_input("Email *", value=profile.get("email", ""), key=f"{key_prefix}_email")
        mobile = st.text_input("Mobile *", value=profile.get("mobile", ""), max_chars=10, key=f"{key_prefix}_mobile")
    else:
        st.caption("Enter details for the person who will travel.")
        name = st.text_input("Full name *", placeholder="Passenger full name", key=f"{key_prefix}_name_o")
        email = st.text_input("Email *", placeholder="passenger@email.com", key=f"{key_prefix}_email_o")
        mobile = st.text_input("Mobile *", placeholder="10-digit mobile", max_chars=10, key=f"{key_prefix}_mobile_o")

    gender = ""
    if require_gender:
        gender = st.selectbox("Gender *", GENDER_OPTIONS, key=f"{key_prefix}_gender")
    else:
        gender = st.selectbox("Gender (optional)", [""] + GENDER_OPTIONS, key=f"{key_prefix}_gender_opt")
        if gender == "":
            gender = ""

    st.markdown("</div>", unsafe_allow_html=True)
    mobile_digits = "".join(c for c in mobile if c.isdigit())
    return {
        "full_name": (name or "").strip(),
        "email": (email or "").strip(),
        "mobile": mobile_digits[-10:] if mobile_digits else "",
        "gender": gender,
        "booking_for": "self" if is_self else "other",
    }


def validate_traveller(traveller: dict, require_gender: bool = False) -> str | None:
    """Return error message or None if valid."""
    if not traveller.get("full_name"):
        return "Full name is required."
    if not traveller.get("email"):
        return "Email is required."
    if not re.match(r"^[\w.\-]+@[\w.\-]+\.\w+$", traveller.get("email", "")):
        return "Enter a valid email address."
    if len(traveller.get("mobile", "")) < 10:
        return "Enter a valid 10-digit mobile number."
    if require_gender and not traveller.get("gender"):
        return "Gender is required for flight booking."
    return None
