"""Premium payment checkout UI."""
import html
import time

import streamlit as st

import api_client
from mock_inventory import OFFERS


def render_order_summary(lines: list, total: int) -> None:
    st.markdown('<div class="tw-checkout-panel"><div class="tw-form-title">Order Summary</div>', unsafe_allow_html=True)
    for label, val in lines:
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;padding:0.3rem 0;font-size:0.9rem">'
            f'<span>{html.escape(label)}</span><span>{html.escape(str(val))}</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;padding:0.75rem 0;font-size:1.25rem;font-weight:800">'
        f'<span>Total</span><span style="color:#e85d04">Rs {total:,}</span></div></div>',
        unsafe_allow_html=True,
    )


def render_premium_payment(
    profile: dict,
    amount_inr: int,
    booking_type: str = "flight",
    user_id: str | None = None,
    token: str | None = None,
) -> dict:
    """Returns {method_label, method_id, coupon, insurance, remember}."""
    st.markdown(
        '<div class="tw-checkout-panel tw-animate-in">'
        '<div class="tw-form-title">Secure Payment</div>'
        '<div style="font-size:0.8rem;opacity:0.75">256-bit secure · PCI compliant (demo) · Instant confirmation</div>',
        unsafe_allow_html=True,
    )
    methods = api_client.get_payment_methods(token, user_id)
    method_labels = [f"{m.get('label', m.get('type'))} ({m.get('last4', m.get('vpa', ''))})" for m in methods]
    choice = st.radio("Saved payment methods", method_labels + ["Add new method"], horizontal=False)
    method_id = methods[0]["id"] if methods and choice != "Add new method" else "new"
    new_method = {}
    if choice == "Add new method" or not methods:
        ptype = st.selectbox("Payment type", ["UPI", "Credit Card", "Wallet"])
        if ptype == "UPI":
            new_method = {"type": "upi", "label": "UPI", "vpa": st.text_input("UPI ID", placeholder="name@upi")}
        elif ptype == "Credit Card":
            c1, c2, c3 = st.columns(3)
            with c1:
                new_method["last4"] = st.text_input("Card last 4", "4242")[-4:]
            with c2:
                st.text_input("Expiry", "12/28")
            with c3:
                st.text_input("CVV", "123", type="password")
            new_method.update({"type": "card", "label": "Visa", "brand": "Visa"})
        else:
            new_method = {"type": "wallet", "label": st.selectbox("Wallet", ["Paytm", "PhonePe", "GPay"])}
    remember = st.checkbox("Remember payment method for next booking", value=True)
    if remember and new_method and choice == "Add new method":
        saved = api_client.save_payment_method(new_method, token, user_id)
        method_id = saved.get("id", method_id)
        if not api_client.is_live():
            st.caption("Not saved to server — Demo Mode")
    coupon = st.text_input("Coupon code", placeholder="TRIPWISE50")
    insurance = st.checkbox("Travel insurance (+Rs 499)", value=False)
    st.markdown("</div>", unsafe_allow_html=True)
    total = amount_inr + (499 if insurance else 0)
    if coupon:
        for o in OFFERS:
            if o["code"] == coupon.upper():
                if "discount_pct" in o:
                    total -= int(amount_inr * o["discount_pct"] / 100)
                elif "discount_inr" in o:
                    total -= min(o["discount_inr"], amount_inr - 1)
    return {
        "method_label": choice,
        "method_id": method_id,
        "new_method": new_method,
        "coupon": coupon,
        "insurance": insurance,
        "remember": remember,
        "total_inr": max(total, 1),
    }


def process_payment_animation() -> None:
    with st.spinner("Processing secure payment..."):
        time.sleep(1.2)
    st.markdown('<div class="tw-success-check">Payment successful</div>', unsafe_allow_html=True)
