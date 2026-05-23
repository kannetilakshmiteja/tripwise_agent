"""Visual aircraft seat map for flight checkout."""
from __future__ import annotations

import hashlib

import streamlit as st

import mock_demo

COLUMNS = ["A", "B", "C", "D", "E", "F"]
ZONE_ROWS = {
    "front": (1, 6),
    "middle": (7, 12),
    "back": (13, 18),
}
ZONE_LABELS = {"front": "Front cabin", "middle": "Middle cabin", "back": "Back cabin"}
BUSINESS_ROWS = (1, 8)


def _seat_meta(seat_id: str) -> dict:
    row = int("".join(c for c in seat_id if c.isdigit()) or "0")
    col = seat_id[-1].upper()
    if col in ("A", "F"):
        pos = "window"
    elif col in ("C", "D"):
        pos = "aisle"
    else:
        pos = "middle"
    if row <= 6:
        zone = "front"
    elif row <= 12:
        zone = "middle"
    else:
        zone = "back"
    return {"seat_id": seat_id, "row": row, "col": col, "seat_position": pos, "seat_zone": zone}


def seat_fee_inr(seat_id: str) -> int:
    """Surcharge per seat — window and front cost more."""
    meta = _seat_meta(seat_id)
    fee = 0
    if meta["seat_position"] == "window":
        fee += 850
    elif meta["seat_position"] == "aisle":
        fee += 450
    elif meta["seat_position"] == "middle":
        fee += 200
    if meta["row"] <= 3:
        fee += 1200
    elif meta["seat_zone"] == "front":
        fee += 600
    elif meta["seat_zone"] == "middle":
        fee += 350
    return fee


def _mock_occupied(flight_id: str, seat_id: str) -> bool:
    """Simulate seats held by other passengers (demo inventory)."""
    h = int(hashlib.md5(f"{flight_id}:{seat_id}".encode()).hexdigest()[:8], 16)
    return h % 10 < 2


def _is_unavailable(flight_id: str, seat_id: str) -> bool:
    if seat_id in mock_demo.get_booked_seats(flight_id):
        return True
    return _mock_occupied(flight_id, seat_id)


def _rows_for_class(travel_class: str) -> list[int]:
    if travel_class == "Business":
        return list(range(BUSINESS_ROWS[0], BUSINESS_ROWS[1] + 1))
    return list(range(1, 19))


def _rows_in_zone(travel_class: str, zone: str) -> list[int]:
    lo, hi = ZONE_ROWS.get(zone, (1, 18))
    return [r for r in _rows_for_class(travel_class) if lo <= r <= hi]


def validate_seat_selection(seats: list[str], pax_count: int, flight_id: str = "") -> str | None:
    if not seats:
        return "Please select at least one seat."
    if len(seats) < pax_count:
        return f"Select {pax_count} seat(s) for all passengers."
    if len(seats) > pax_count:
        return f"Select only {pax_count} seat(s)."
    if flight_id:
        for s in seats:
            if not mock_demo.is_seat_available(flight_id, s):
                return f"Seat {s} was just booked by another traveller. Choose another seat."
    return None


def render_checkout_substeps(current: str) -> None:
    parts = []
    for key, label in [("traveller", "Traveller"), ("seat", "Seat"), ("pay", "Payment")]:
        cls = "tw-checkout-sub-active" if key == current else "tw-checkout-sub-pending"
        parts.append(f'<span class="tw-checkout-sub {cls}">{label}</span>')
    st.markdown(f'<div class="tw-checkout-substeps">{"".join(parts)}</div>', unsafe_allow_html=True)


def render_seat_map(
    pax_count: int,
    travel_class: str = "Economy",
    key_prefix: str = "seat",
    flight_id: str = "",
) -> dict:
    """Interactive seat grid for the active cabin zone only."""
    fid = str(flight_id or key_prefix)
    st.markdown('<div class="tw-seat-map"><div class="tw-form-title">Select your seat</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tw-seat-legend">'
        '<span class="tw-seat-chip tw-seat-window">Window +Rs 850</span>'
        '<span class="tw-seat-chip tw-seat-aisle">Aisle +Rs 450</span>'
        '<span class="tw-seat-chip tw-seat-extra">Rows 1–3 +Rs 1200</span>'
        '<span class="tw-seat-chip tw-seat-booked">Gray = booked</span>'
        "</div>",
        unsafe_allow_html=True,
    )

    sel_key = f"{key_prefix}_selected"
    zone_key = f"{key_prefix}_zone"
    prev_zone_key = f"{key_prefix}_zone_prev"

    if sel_key not in st.session_state:
        st.session_state[sel_key] = []

    zone = st.radio(
        "Cabin zone",
        ["front", "middle", "back"],
        horizontal=True,
        format_func=lambda z: ZONE_LABELS.get(z, z.title()),
        key=zone_key,
    )
    if st.session_state.get(prev_zone_key) != zone:
        st.session_state[sel_key] = []
        st.session_state[prev_zone_key] = zone

    pref = st.radio("Seat preference", ["Any", "Window", "Aisle"], horizontal=True, key=f"{key_prefix}_pref")
    zone_rows = _rows_in_zone(travel_class, zone)
    st.caption(f"Showing **{ZONE_LABELS[zone]}** · rows **{zone_rows[0]}–{zone_rows[-1]}**" if zone_rows else "No rows in this zone.")

    if st.button("Suggest best seat in this zone", key=f"{key_prefix}_suggest"):
        found = None
        for row in zone_rows:
            for col in COLUMNS:
                seat_id = f"{row}{col}"
                if _is_unavailable(fid, seat_id):
                    continue
                meta = _seat_meta(seat_id)
                if pref == "Window" and meta["seat_position"] != "window":
                    continue
                if pref == "Aisle" and meta["seat_position"] != "aisle":
                    continue
                found = seat_id
                break
            if found:
                break
        if found:
            st.session_state[sel_key] = [found]
            st.rerun()
        else:
            st.warning("No free seat in this zone. Try another zone or preference.")

    nose = {"front": "FRONT ✈", "middle": "MID ✈", "back": "BACK ✈"}[zone]
    st.markdown(f'<div class="tw-seat-fuselage"><div class="tw-seat-nose">{nose} — {ZONE_LABELS[zone]}</div>', unsafe_allow_html=True)
    st.caption("A · B · C  |  aisle  |  D · E · F")

    selected: list[str] = list(st.session_state.get(sel_key, []))

    if not zone_rows:
        st.warning("No seats in this zone for selected class.")
    else:
        st.markdown(
            '<div class="tw-seat-grid-head">'
            '<span></span><span>A</span><span>B</span><span>C</span>'
            '<span class="tw-seat-aisle">||</span>'
            '<span>D</span><span>E</span><span>F</span></div>',
            unsafe_allow_html=True,
        )
        for row in zone_rows:
            extra = " · XL" if row <= 3 else ""
            cols = st.columns([0.55, 1, 1, 1, 0.2, 1, 1, 1])
            with cols[0]:
                st.markdown(f"**{row}**{extra}", unsafe_allow_html=True)
            seat_cols = [cols[1], cols[2], cols[3], cols[5], cols[6], cols[7]]
            for col_letter, sc in zip(COLUMNS, seat_cols):
                seat_id = f"{row}{col_letter}"
                unavailable = _is_unavailable(fid, seat_id)
                is_sel = seat_id in selected
                fee = seat_fee_inr(seat_id)
                with sc:
                    if unavailable:
                        st.button(
                            f"{seat_id} ✕",
                            key=f"{key_prefix}_{zone}_{seat_id}_x",
                            disabled=True,
                            use_container_width=True,
                        )
                    elif st.button(
                        f"{seat_id} (+{fee})",
                        key=f"{key_prefix}_{zone}_{seat_id}",
                        type="primary" if is_sel else "secondary",
                        disabled=len(selected) >= pax_count and not is_sel,
                        use_container_width=True,
                    ):
                        if is_sel:
                            selected = [s for s in selected if s != seat_id]
                        else:
                            selected = selected + [seat_id] if len(selected) < pax_count else selected
                        st.session_state[sel_key] = selected
                        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    total_fees = sum(seat_fee_inr(s) for s in selected)
    breakdown = [f"{s}: +Rs {seat_fee_inr(s):,}" for s in selected]

    if selected:
        labels = []
        for sid in selected:
            m = _seat_meta(sid)
            labels.append(f"**{sid}** ({m['seat_position'].title()}, +Rs {seat_fee_inr(sid):,})")
        st.success("Selected: " + " · ".join(labels))
        st.caption(f"Seat surcharge total: **Rs {total_fees:,}**")
    else:
        st.info(f"Choose up to **{pax_count}** seat(s) in **{ZONE_LABELS[zone]}**. Gray = already booked.")

    st.markdown("</div>", unsafe_allow_html=True)

    primary = selected[0] if selected else ""
    meta = _seat_meta(primary) if primary else {}
    return {
        "seats": selected,
        "seat": primary,
        "seat_position": meta.get("seat_position", ""),
        "seat_zone": meta.get("seat_zone", zone),
        "seat_fees_inr": total_fees,
        "seat_fee_breakdown": breakdown,
    }
