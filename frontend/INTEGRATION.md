# TripWise — Person 1 ↔ Person 2 Integration

Person 1 owns **frontend/** only. Person 2 owns **backend/**.

## Run together

```bash
# Terminal 1 — Person 2
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 — Person 1
cd frontend
set TRIPWISE_API_URL=http://127.0.0.1:8000
streamlit run app.py
```

Navbar: **Backend Connected** (green) or **Demo Mode** (orange).

## Person 1 calls (via api_client.py only)

| Function | Method | Endpoint |
|----------|--------|----------|
| check_api_health | GET | /health |
| send_otp | POST | /auth/send-otp |
| verify_otp | POST | /auth/verify-otp |
| save_user_profile | POST | /users/profile |
| get_user_me | GET | /users/me |
| post_chat | POST | /chat |
| post_flight_search | POST | /flights/search |
| post_flight_book | POST | /flights/book |
| post_hotel_search | POST | /hotels/search |
| post_hotel_book | POST | /hotels/book |
| get_my_bookings | GET | /bookings/me |
| cancel_preview | POST | /bookings/{id}/cancel/preview |
| cancel_booking | POST | /bookings/{id}/cancel |
| get_payment_methods | GET | /payments/methods |
| charge_payment | POST | /payments/charge |
| get_refund | GET | /refund/{id} |

## Demo mode (Person 2 offline)

- OTP: any mobile, use **123456**
- All data in-memory mock (mock_demo.py)
- UI fully functional for demos

## Request examples

### POST /auth/send-otp
```json
{ "mobile": "9876543210" }
```

### POST /auth/verify-otp
```json
{ "mobile": "9876543210", "otp": "123456" }
```
Response:
```json
{ "token": "jwt...", "user_id": "u1", "profile_complete": false }
```

### POST /flights/search
```json
{ "from": "DEL", "to": "DXB", "passengers": 1, "class": "Economy" }
```
Response flight object must include:
```json
{
  "id": "FL-104",
  "airline": "IndiGo",
  "flight_no": "6E-1451",
  "price_inr": 19500,
  "flight_status": "OnTime",
  "delay_minutes": 0,
  "fare_type": "Refundable"
}
```

### POST /hotels/search
```json
{ "city": "Dubai", "rooms": 1 }
```
Response hotel object must include:
```json
{
  "id": "HT-201",
  "name": "Marina Bay Resort",
  "image_url": "https://...",
  "images": ["https://..."],
  "rating": 4.7,
  "reviews_count": 1240,
  "cancellation_policy": "Free cancellation until 48h before check-in"
}
```

### POST /flights/book
```json
{
  "flight": { "id": "FL-104" },
  "profile": { "full_name", "email", "mobile", "gender" },
  "payment": { "method_id": "pm_upi" },
  "coupon": "TRIPWISE50",
  "insurance": true,
  "seat": "12A",
  "seats": ["12A"],
  "seat_position": "window",
  "seat_zone": "middle",
  "booking_for": "self"
}
```

### POST /hotels/book (optional fields)
```json
{
  "hotel": { "id": "HT-201" },
  "profile": { "full_name", "email", "mobile" },
  "nights": 2,
  "room_prefs": {
    "room_type": "Deluxe",
    "bed": "King",
    "guests": 2,
    "smoking": "Non-smoking",
    "floor_preference": "High floor",
    "special_request": ""
  }
}
```

### POST /bookings/{id}/cancel/preview
Response:
```json
{
  "refund_eligible_inr": 62400,
  "cancellation_fee_inr": 12000,
  "policy_text": "Refundable fare — standard fee"
}
```
