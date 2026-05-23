"""Hotel room preferences and dynamic pricing at checkout."""
import streamlit as st

ROOM_MULTIPLIER = {"Standard": 1.0, "Deluxe": 1.38, "Suite": 1.85}
BED_SURCHARGE = {"King": 950, "Twin": 0, "Double": 550}
FLOOR_SURCHARGE = {"No preference": 0, "Low floor": 250, "High floor": 750}
SMOKING_SURCHARGE = {"Non-smoking": 0, "Smoking": 450}


def calc_hotel_total(base_price_night: int, nights: int, prefs: dict) -> tuple[int, list[tuple[str, str]]]:
    """Return (total_inr, order_summary_lines)."""
    mult = ROOM_MULTIPLIER.get(prefs.get("room_type", "Standard"), 1.0)
    base_adj = int(base_price_night * mult)
    bed = BED_SURCHARGE.get(prefs.get("bed", "Twin"), 0)
    floor = FLOOR_SURCHARGE.get(prefs.get("floor_preference", "No preference"), 0)
    smoke = SMOKING_SURCHARGE.get(prefs.get("smoking", "Non-smoking"), 0)
    guests = int(prefs.get("guests", 2))
    guest_extra = max(0, guests - 2) * 400
    per_night = base_adj + bed + floor + smoke + guest_extra
    total = per_night * max(1, nights)
    lines = [
        (f"Base rate ({prefs.get('room_type', 'Standard')})", f"Rs {base_adj:,}/night"),
        (f"Bed ({prefs.get('bed', '')})", f"+Rs {bed:,}/night" if bed else "Included"),
        (f"Floor ({prefs.get('floor_preference', '')})", f"+Rs {floor:,}/night" if floor else "Included"),
        (f"Smoking", f"+Rs {smoke:,}/night" if smoke else "Non-smoking"),
    ]
    if guest_extra:
        lines.append((f"Extra guests ({guests - 2})", f"+Rs {guest_extra:,}/night"))
    lines.append((f"{nights} night(s) × Rs {per_night:,}", f"Rs {total:,}"))
    return total, lines


def render_hotel_preferences(key_prefix: str = "htp", base_price_night: int = 0, nights: int = 1) -> dict:
    st.markdown('<div class="tw-hotel-prefs-panel"><div class="tw-form-title">Room preferences</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        room_type = st.selectbox("Room type", list(ROOM_MULTIPLIER.keys()), key=f"{key_prefix}_room")
        bed = st.selectbox("Bed type", list(BED_SURCHARGE.keys()), key=f"{key_prefix}_bed")
        guests = st.number_input("Guests", 1, 4, 2, key=f"{key_prefix}_guests")
    with c2:
        smoking = st.selectbox("Smoking", list(SMOKING_SURCHARGE.keys()), key=f"{key_prefix}_smoke")
        floor = st.selectbox("Floor preference", list(FLOOR_SURCHARGE.keys()), key=f"{key_prefix}_floor")
    special = st.text_area("Special request (optional)", placeholder="Late check-in, quiet room…", key=f"{key_prefix}_note")
    prefs = {
        "room_type": room_type,
        "bed": bed,
        "guests": int(guests),
        "smoking": smoking,
        "floor_preference": floor,
        "special_request": (special or "").strip(),
    }
    if base_price_night > 0:
        total, lines = calc_hotel_total(base_price_night, nights, prefs)
        prefs["estimated_total_inr"] = total
        prefs["price_lines"] = lines
        st.markdown("**Estimated room total**")
        for lbl, val in lines[-3:]:
            st.caption(f"{lbl}: {val}")
        st.markdown(f'<p class="tw-hotel-price-total">Rs {total:,} for {nights} night(s)</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    return prefs
