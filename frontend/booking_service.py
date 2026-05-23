"""Booking operations — search, confirm, coupons."""
from datetime import datetime, timezone

from mock_inventory import make_pnr, search_flights, search_hotels, OFFERS
from user_store import add_booking, load_profile


def apply_coupon(price: int, code: str) -> tuple[int, str]:
    code_u = (code or "").upper().strip()
    for offer in OFFERS:
        if offer["code"] == code_u:
            if "discount_pct" in offer:
                discount = int(price * offer["discount_pct"] / 100)
                return price - discount, f"Applied {code_u}: -₹{discount}"
            if "discount_inr" in offer:
                d = min(offer["discount_inr"], price - 1)
                return price - d, f"Applied {code_u}: -₹{d}"
    return price, "Invalid coupon"


def book_flight(flight: dict, profile: dict, coupon: str = "", insurance: bool = False) -> dict:
    price = flight.get("price_total", flight.get("price_inr", 0))
    final, coupon_msg = apply_coupon(price, coupon)
    if insurance:
        final += 499
    booking = {
        "type": "flight",
        "booking_id": f"TW-{datetime.now().strftime('%Y%m%d')}-{make_pnr()}",
        "pnr": make_pnr(),
        "flight": flight,
        "passenger": profile.get("full_name", "Guest"),
        "amount_inr": final,
        "insurance": insurance,
        "coupon_msg": coupon_msg,
        "status": "Confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    add_booking(booking)
    return booking


def book_hotel(hotel: dict, profile: dict, nights: int = 1, coupon: str = "") -> dict:
    price = hotel.get("price_night", 0) * nights
    final, coupon_msg = apply_coupon(price, coupon)
    booking = {
        "type": "hotel",
        "booking_id": f"TW-H-{datetime.now().strftime('%Y%m%d')}-{make_pnr()}",
        "hotel": hotel,
        "guest": profile.get("full_name", "Guest"),
        "nights": nights,
        "amount_inr": final,
        "coupon_msg": coupon_msg,
        "status": "Confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    add_booking(booking)
    return booking
