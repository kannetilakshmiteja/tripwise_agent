"""Demo-mode fallbacks when Person 2 API is offline."""
from datetime import datetime, timezone

from config import DEMO_OTP
from mock_inventory import make_pnr, search_flights, search_hotels, OFFERS

_demo_users: dict[str, dict] = {}
_demo_bookings: list[dict] = []
_demo_payments: dict[str, list] = {}
_demo_refunds: list[dict] = []


def is_demo_mode(api_connected: bool) -> bool:
    return not api_connected


def demo_send_otp(mobile: str) -> dict:
    m = _norm_mobile(mobile)
    return {"success": True, "message": f"OTP sent to {m}", "demo_otp": DEMO_OTP, "mode": "mock"}


def demo_verify_otp(mobile: str, otp: str) -> dict:
    m = _norm_mobile(mobile)
    if otp.strip() != DEMO_OTP:
        return {"success": False, "error": "Invalid OTP. Demo OTP is 123456"}
    uid = f"user_{m}"
    existing = _demo_users.get(m)
    return {
        "success": True,
        "token": f"demo_token_{m}",
        "user_id": uid,
        "profile_complete": bool(
            existing
            and existing.get("full_name")
            and existing.get("email")
        ),
        "mode": "mock",
    }


def demo_save_profile(mobile: str, profile: dict) -> dict:
    m = _norm_mobile(mobile)
    profile = {**profile, "mobile": m, "user_id": f"user_{m}"}
    _demo_users[m] = profile
    return {"success": True, "profile": profile, "mode": "mock"}


def demo_get_profile(mobile: str) -> dict | None:
    return _demo_users.get(_norm_mobile(mobile))


def demo_get_payment_methods(user_id: str) -> list:
    return _demo_payments.get(user_id, [
        {"id": "pm_upi", "type": "upi", "label": "UPI", "vpa": "demo@upi"},
        {"id": "pm_card", "type": "card", "label": "Visa", "last4": "4242", "brand": "Visa"},
    ])


def demo_save_payment_method(user_id: str, method: dict) -> dict:
    methods = _demo_payments.setdefault(user_id, demo_get_payment_methods(user_id))
    method["id"] = method.get("id") or f"pm_{len(methods)}"
    methods.append(method)
    return method


def get_booked_seats(flight_id: str) -> set[str]:
    """Seats already sold on this flight (all customers in demo)."""
    fid = str(flight_id)
    taken: set[str] = set()
    for b in _demo_bookings:
        if b.get("type") != "flight" or b.get("status") == "Cancelled":
            continue
        fl = b.get("flight") or {}
        if str(fl.get("id")) != fid:
            continue
        for s in b.get("seats") or []:
            if s:
                taken.add(str(s))
        if b.get("seat"):
            taken.add(str(b["seat"]))
    return taken


def is_seat_available(flight_id: str, seat_id: str) -> bool:
    return seat_id not in get_booked_seats(flight_id)


def demo_book_flight(flight: dict, profile: dict, **kwargs) -> dict:
    fid = str(flight.get("id", ""))
    for s in kwargs.get("seats") or ([kwargs.get("seat")] if kwargs.get("seat") else []):
        if s and not is_seat_available(fid, str(s)):
            return {"error": f"Seat {s} is no longer available. Please pick another seat.", "success": False}
    price = flight.get("price_total", flight.get("price_inr", 0))
    seat_fees = int(kwargs.get("seat_fees_inr", 0))
    price = price + seat_fees
    coupon = kwargs.get("coupon", "")
    insurance = kwargs.get("insurance", False)
    final, coupon_msg = _apply_coupon(price, coupon)
    if insurance:
        final += 499
    booking = {
        "type": "flight",
        "booking_id": f"TW-{datetime.now().strftime('%Y%m%d')}-{make_pnr()}",
        "pnr": make_pnr(),
        "flight": flight,
        "passenger": profile.get("full_name", "Guest"),
        "email": profile.get("email", ""),
        "mobile": profile.get("mobile", ""),
        "booking_for": kwargs.get("booking_for", "self"),
        "amount_inr": final,
        "insurance": insurance,
        "coupon_msg": coupon_msg,
        "status": "Confirmed",
        "flight_status": flight.get("flight_status", "OnTime"),
        "delay_minutes": flight.get("delay_minutes", 0),
        "fare_type": flight.get("fare_type", "Refundable"),
        "payment_method": kwargs.get("payment_method", "UPI"),
        "gender": profile.get("gender") or kwargs.get("gender", ""),
        "seat": kwargs.get("seat", ""),
        "seats": kwargs.get("seats", []),
        "seat_position": kwargs.get("seat_position", ""),
        "seat_zone": kwargs.get("seat_zone", ""),
        "seat_fees_inr": seat_fees,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "mock",
    }
    _demo_bookings.append(booking)
    return booking


def demo_book_hotel(hotel: dict, profile: dict, nights: int = 1, **kwargs) -> dict:
    room_prefs = kwargs.get("room_prefs") or {}
    base_night = hotel.get("price_night", 0)
    price = int(kwargs.get("room_total_inr") or base_night * nights)
    final, coupon_msg = _apply_coupon(price, kwargs.get("coupon", ""))
    if kwargs.get("insurance"):
        final += 499
    booking = {
        "type": "hotel",
        "booking_id": f"TW-H-{datetime.now().strftime('%Y%m%d')}-{make_pnr()}",
        "hotel": hotel,
        "guest": profile.get("full_name", "Guest"),
        "email": profile.get("email", ""),
        "mobile": profile.get("mobile", ""),
        "booking_for": kwargs.get("booking_for", "self"),
        "nights": nights,
        "amount_inr": final,
        "coupon_msg": coupon_msg,
        "cancellation_policy": hotel.get("cancellation_policy", ""),
        "image_url": hotel.get("image_url", ""),
        "status": "Confirmed",
        "payment_method": kwargs.get("payment_method", "UPI"),
        "room_prefs": room_prefs,
        "room_total_inr": price,
        "gender": profile.get("gender") or kwargs.get("gender", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "mock",
    }
    _demo_bookings.append(booking)
    return booking


def demo_get_bookings(mobile: str) -> list:
    m = _norm_mobile(mobile)
    if not m:
        return []
    return [b for b in _demo_bookings if _norm_mobile(b.get("mobile", "")) == m]


def demo_cancel_preview(booking_id: str) -> dict:
    b = _find_booking(booking_id)
    if not b:
        return {"error": "Booking not found"}
    from policy_engine import calc_refund
    return calc_refund(b, preview=True)


def demo_cancel_booking(booking_id: str) -> dict:
    b = _find_booking(booking_id)
    if not b:
        return {"error": "Booking not found"}
    from policy_engine import calc_refund
    est = calc_refund(b, preview=True)
    b["status"] = "Cancelled"
    refund = {
        "refund_id": f"RF-{make_pnr()}",
        "booking_id": booking_id,
        "amount_inr": est["refund_eligible_inr"],
        "status": "Processing",
        "timeline": est.get("timeline", []),
    }
    _demo_refunds.append(refund)
    return {"success": True, "booking": b, "refund": refund, **est}


def demo_get_refunds(mobile: str) -> list:
    return _demo_refunds


def demo_simulate_delay(booking_id: str) -> bool:
    b = _find_booking(booking_id)
    if b and b.get("type") == "flight":
        b["flight_status"] = "Delayed"
        b["delay_minutes"] = 260
        return True
    return False


def _find_booking(booking_id: str) -> dict | None:
    for b in _demo_bookings:
        if b.get("booking_id") == booking_id:
            return b
    return None


def _norm_mobile(mobile: str) -> str:
    return "".join(c for c in mobile if c.isdigit())[-10:]


def _apply_coupon(price: int, code: str) -> tuple[int, str]:
    code_u = (code or "").upper().strip()
    for offer in OFFERS:
        if offer["code"] == code_u:
            if "discount_pct" in offer:
                d = int(price * offer["discount_pct"] / 100)
                return price - d, f"Applied {code_u}: -Rs {d}"
            if "discount_inr" in offer:
                d = min(offer["discount_inr"], price - 1)
                return price - d, f"Applied {code_u}: -Rs {d}"
    return price, "No coupon applied" if code else ""
