"""TripWise frontend configuration."""
import os

API_BASE_URL = os.getenv("TRIPWISE_API_URL", "http://127.0.0.1:8000")
AUTH_REGISTER = f"{API_BASE_URL}/auth/register"
AUTH_LOGIN = f"{API_BASE_URL}/auth/login"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
BOOKING_ENDPOINT = f"{API_BASE_URL}/booking"
REFUND_ENDPOINT = f"{API_BASE_URL}/refund"
POLICIES_ENDPOINT = f"{API_BASE_URL}/policies"
ESCALATIONS_ENDPOINT = f"{API_BASE_URL}/escalations"
FLIGHT_SEARCH_ENDPOINT = f"{API_BASE_URL}/flights/search"
FLIGHT_BOOK_ENDPOINT = f"{API_BASE_URL}/flights/book"
HOTEL_SEARCH_ENDPOINT = f"{API_BASE_URL}/hotels/search"
HOTEL_BOOK_ENDPOINT = f"{API_BASE_URL}/hotels/book"
AUTH_SEND_OTP = f"{API_BASE_URL}/auth/send-otp"
AUTH_VERIFY_OTP = f"{API_BASE_URL}/auth/verify-otp"
USERS_ME = f"{API_BASE_URL}/users/me"
USERS_PROFILE = f"{API_BASE_URL}/users/profile"
BOOKINGS_ME = f"{API_BASE_URL}/bookings/me"
BOOKINGS_CANCEL_PREVIEW = f"{API_BASE_URL}/bookings/{{booking_id}}/cancel/preview"
BOOKINGS_CANCEL = f"{API_BASE_URL}/bookings/{{booking_id}}/cancel"
PAYMENTS_METHODS = f"{API_BASE_URL}/payments/methods"
PAYMENTS_METHODS_POST = f"{API_BASE_URL}/payments/methods"
PAYMENTS_CHARGE = f"{API_BASE_URL}/payments/charge"
REQUEST_TIMEOUT = int(os.getenv("TRIPWISE_TIMEOUT", "30"))
DEMO_OTP = "123456"

PROJECT_NAME = "TripWise Travel Services"
TAGLINE = "Agentic AI Travel Booking & Customer Support"

CITIES = ["Delhi (DEL)", "Dubai (DXB)", "Mumbai (BOM)", "Goa (GOI)", "Bangalore (BLR)"]
CITY_CODES = {
    "Delhi (DEL)": "DEL",
    "Dubai (DXB)": "DXB",
    "Mumbai (BOM)": "BOM",
    "Goa (GOI)": "GOI",
    "Bangalore (BLR)": "BLR",
}

AGENT_PIPELINE = []
