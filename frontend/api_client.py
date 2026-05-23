"""Single gateway to Person 2 FastAPI — mock fallback in demo mode."""
import requests

from config import (
    AUTH_REGISTER,
    AUTH_LOGIN,
    API_BASE_URL,
    AUTH_SEND_OTP,
    AUTH_VERIFY_OTP,
    BOOKING_ENDPOINT,
    BOOKINGS_CANCEL,
    BOOKINGS_CANCEL_PREVIEW,
    BOOKINGS_ME,
    CHAT_ENDPOINT,
    FLIGHT_BOOK_ENDPOINT,
    FLIGHT_SEARCH_ENDPOINT,
    HEALTH_ENDPOINT,
    HOTEL_BOOK_ENDPOINT,
    HOTEL_SEARCH_ENDPOINT,
    PAYMENTS_CHARGE,
    PAYMENTS_METHODS,
    PAYMENTS_METHODS_POST,
    REFUND_ENDPOINT,
    REQUEST_TIMEOUT,
    USERS_ME,
    USERS_PROFILE,
)
from mock_data import generate_mock_chat_response
import mock_demo

def register_user(full_name: str, email: str, mobile: str, password: str) -> dict:
    result = _post(AUTH_REGISTER, {
        "full_name": full_name,
        "email": email,
        "mobile": mobile,
        "password": password
    })

    if result:
        return result

    return {
        "success": False,
        "error": "Registration failed"
    }


def login_user(email: str, password: str) -> dict:
    result = _post(AUTH_LOGIN, {
        "email": email,
        "password": password
    })

    if result:
        return result

    return {
        "success": False,
        "error": "Invalid email or password"
    }
def _headers(token: str | None = None) -> dict:
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def check_api_health() -> bool:
    try:
        r = requests.get(HEALTH_ENDPOINT, timeout=3)
        return r.ok
    except requests.RequestException:
        try:
            r = requests.get(API_BASE_URL, timeout=3)
            return r.ok
        except requests.RequestException:
            return False


def is_live() -> bool:
    return check_api_health()


def _get(url: str, token: str | None = None) -> dict | None:
    try:
        r = requests.get(url, headers=_headers(token), timeout=REQUEST_TIMEOUT)
        if r.ok:
            return r.json()
    except requests.RequestException:
        pass
    return None


def _post(url: str, payload: dict, token: str | None = None) -> dict | None:
    try:
        r = requests.post(url, json=payload, headers=_headers(token), timeout=REQUEST_TIMEOUT)
        if r.ok:
            return r.json()
    except requests.RequestException:
        pass
    return None


# --- Auth ---
def send_otp(mobile: str) -> dict:
    live = _post(AUTH_SEND_OTP, {"mobile": mobile})
    if live:
        live["mode"] = "live"
        return live
    return mock_demo.demo_send_otp(mobile)


def verify_otp(mobile: str, otp: str) -> dict:
    live = _post(AUTH_VERIFY_OTP, {"mobile": mobile, "otp": otp})
    if live:
        live["mode"] = "live"
        return live
    return mock_demo.demo_verify_otp(mobile, otp)


def save_user_profile(profile: dict, token: str | None = None) -> dict:
    live = _post(USERS_PROFILE, profile, token)
    if live:
        live["mode"] = "live"
        return live
    mobile = profile.get("mobile", "")
    return mock_demo.demo_save_profile(mobile, profile)


def get_user_me(token: str | None = None, mobile: str | None = None) -> dict | None:
    live = _get(USERS_ME, token)
    if live:
        live["mode"] = "live"
        return live
    if mobile:
        return mock_demo.demo_get_profile(mobile)
    return None


# --- Chat ---
def post_chat(message: str, booking_id: str | None = None, context: dict | None = None, token: str | None = None) -> dict:
    payload = {"message": message}
    if booking_id:
        payload["booking_id"] = booking_id
    if context:
        payload["context"] = context
    live = _post(CHAT_ENDPOINT, payload, token)
    if live:
        live.setdefault("mode", "live")
        return live
    data = generate_mock_chat_response(message)
    data["api_note"] = "Demo Mode — start Person 2 on port 8000 for live API"
    return data


# --- Flights / Hotels ---
def post_flight_search(from_code: str, to_code: str, **kwargs) -> dict:
    travel_class = kwargs.pop("travel_class", kwargs.pop("class", "Economy"))
    passengers = kwargs.get("passengers", 1)
    payload = {"from": from_code, "to": to_code, "passengers": passengers, "class": travel_class, **kwargs}
    live = _post(FLIGHT_SEARCH_ENDPOINT, payload)
    if live:
        live["mode"] = "live"
        return live
    from mock_inventory import search_flights
    return {"flights": search_flights(from_code, to_code, passengers, travel_class), "mode": "mock"}


def post_flight_book(flight: dict, profile: dict, **kwargs) -> dict:
    payload = {"flight": flight, "profile": profile, **kwargs}
    token = kwargs.pop("token", None)
    live = _post(FLIGHT_BOOK_ENDPOINT, payload, token)
    if live:
        live["mode"] = "live"
        return live
    return mock_demo.demo_book_flight(flight, profile, **kwargs)


def post_hotel_search(city: str, **kwargs) -> dict:
    live = _post(HOTEL_SEARCH_ENDPOINT, {"city": city, **kwargs})
    if live:
        live["mode"] = "live"
        return live
    from mock_inventory import search_hotels
    return {"hotels": search_hotels(city, kwargs.get("rooms", 1)), "mode": "mock"}


def post_hotel_book(hotel: dict, profile: dict, **kwargs) -> dict:
    payload = {"hotel": hotel, "profile": profile, **kwargs}
    token = kwargs.pop("token", None)
    live = _post(HOTEL_BOOK_ENDPOINT, payload, token)
    if live:
        live["mode"] = "live"
        return live
    nights = kwargs.pop("nights", 1)
    return mock_demo.demo_book_hotel(hotel, profile, nights=nights, **kwargs)


# --- Bookings ---
def get_my_bookings(token: str | None = None, mobile: str | None = None) -> list:
    live = _get(BOOKINGS_ME, token)
    if live:
        return live if isinstance(live, list) else live.get("bookings", [])
    return mock_demo.demo_get_bookings(mobile or "")


def cancel_preview(booking_id: str, token: str | None = None) -> dict:
    url = BOOKINGS_CANCEL_PREVIEW.replace("{booking_id}", booking_id)
    live = _post(url, {}, token)
    if live:
        live["mode"] = "live"
        return live
    return mock_demo.demo_cancel_preview(booking_id)


def cancel_booking(booking_id: str, token: str | None = None) -> dict:
    url = BOOKINGS_CANCEL.replace("{booking_id}", booking_id)
    live = _post(url, {}, token)
    if live:
        live["mode"] = "live"
        return live
    return mock_demo.demo_cancel_booking(booking_id)


def get_booking(booking_id: str, token: str | None = None) -> dict | None:
    live = _get(f"{BOOKING_ENDPOINT}/{booking_id}", token)
    if live:
        return live
    for b in mock_demo.demo_get_bookings(""):
        if b.get("booking_id") == booking_id:
            return b
    return None


# --- Payments ---
def save_payment_method(method: dict, token: str | None = None, user_id: str | None = None) -> dict:
    live = _post(PAYMENTS_METHODS_POST, method, token)
    if live:
        live["mode"] = "live"
        return live
    return mock_demo.demo_save_payment_method(user_id or "demo", method)


def get_payment_methods(token: str | None = None, user_id: str | None = None) -> list:
    live = _get(PAYMENTS_METHODS, token)
    if live:
        return live if isinstance(live, list) else live.get("methods", [])
    return mock_demo.demo_get_payment_methods(user_id or "demo")


def charge_payment(booking_id: str, method_id: str, amount_inr: int, token: str | None = None) -> dict:
    live = _post(PAYMENTS_CHARGE, {"booking_id": booking_id, "method_id": method_id, "amount_inr": amount_inr}, token)
    if live:
        live["mode"] = "live"
        return live
    return {"success": True, "txn_id": f"TXN-{booking_id}", "mode": "mock"}


def get_refund(refund_id: str, token: str | None = None) -> dict | None:
    live = _get(f"{REFUND_ENDPOINT}/{refund_id}", token)
    if live:
        return live
    for r in mock_demo.demo_get_refunds(""):
        if r.get("refund_id") == refund_id:
            return r
    return None


def get_all_refunds(mobile: str) -> list:
    return mock_demo.demo_get_refunds(mobile)
