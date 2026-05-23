"""Mock flight and hotel inventory."""
import random

FLIGHT_STATUSES = ["OnTime", "OnTime", "Scheduled", "Delayed", "OnTime"]

FLIGHTS_DB = [
    {"id": "FL-101", "from": "DEL", "to": "DXB", "airline": "Emirates", "flight_no": "EK-513", "dep": "02:35", "arr": "05:10", "duration": "3h 05m", "stops": 0, "price_inr": 28400, "class": "Economy", "flight_status": "OnTime", "delay_minutes": 0, "fare_type": "Refundable"},
    {"id": "FL-102", "from": "DEL", "to": "DXB", "airline": "Emirates", "flight_no": "EK-515", "dep": "08:40", "arr": "11:15", "duration": "3h 05m", "stops": 0, "price_inr": 31200, "class": "Economy", "flight_status": "OnTime", "delay_minutes": 0, "fare_type": "Refundable"},
    {"id": "FL-103", "from": "DEL", "to": "DXB", "airline": "Air India", "flight_no": "AI-996", "dep": "11:20", "arr": "16:45", "duration": "6h 55m", "stops": 1, "price_inr": 22800, "class": "Economy", "flight_status": "Delayed", "delay_minutes": 90, "fare_type": "Partial"},
    {"id": "FL-104", "from": "DEL", "to": "DXB", "airline": "IndiGo", "flight_no": "6E-1451", "dep": "14:05", "arr": "19:30", "duration": "6h 55m", "stops": 1, "price_inr": 19500, "class": "Economy", "flight_status": "OnTime", "delay_minutes": 0, "fare_type": "Refundable"},
    {"id": "FL-105", "from": "DEL", "to": "DXB", "airline": "SpiceJet", "flight_no": "SG-11", "dep": "18:50", "arr": "23:40", "duration": "5h 20m", "stops": 1, "price_inr": 18200, "class": "Economy", "flight_status": "OnTime", "delay_minutes": 0, "fare_type": "Non-refundable"},
    {"id": "FL-106", "from": "DEL", "to": "DXB", "airline": "Flydubai", "flight_no": "FZ-445", "dep": "06:15", "arr": "08:50", "duration": "3h 05m", "stops": 0, "price_inr": 24100, "class": "Economy", "flight_status": "Scheduled", "delay_minutes": 0, "fare_type": "Refundable"},
    {"id": "FL-107", "from": "DEL", "to": "GOI", "airline": "IndiGo", "flight_no": "6E-204", "dep": "07:00", "arr": "09:25", "duration": "2h 25m", "stops": 0, "price_inr": 4500, "class": "Economy", "flight_status": "OnTime", "delay_minutes": 0, "fare_type": "Refundable"},
    {"id": "FL-108", "from": "DEL", "to": "BOM", "airline": "Vistara", "flight_no": "UK-945", "dep": "09:30", "arr": "11:45", "duration": "2h 15m", "stops": 0, "price_inr": 5200, "class": "Economy", "flight_status": "Cancelled", "delay_minutes": 0, "fare_type": "Refundable"},
    {"id": "FL-109", "from": "DEL", "to": "DXB", "airline": "Emirates", "flight_no": "EK-511", "dep": "22:10", "arr": "00:45", "duration": "3h 05m", "stops": 0, "price_inr": 35800, "class": "Business", "flight_status": "OnTime", "delay_minutes": 0, "fare_type": "Refundable"},
]

HOTEL_IMAGES = {
    "HT-201": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600",
    "HT-202": "https://images.unsplash.com/photo-1582719508461-905c593771e0?w=600",
    "HT-203": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=600",
    "HT-204": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600",
    "HT-205": "https://images.unsplash.com/photo-1596435209908-7fb634d41e23?w=600",
    "HT-206": "https://images.unsplash.com/photo-1521783988139-89397d761eb6?w=600",
}

HOTELS_DB = [
    {"id": "HT-201", "name": "Marina Bay Resort", "city": "Dubai", "stars": 5, "price_night": 12500, "amenities": ["Pool", "Spa", "Breakfast"], "rating": 4.7, "reviews_count": 1240, "cancellation_policy": "Free cancellation until 48 hours before check-in", "image_url": HOTEL_IMAGES["HT-201"], "images": [HOTEL_IMAGES["HT-201"], HOTEL_IMAGES["HT-202"]]},
    {"id": "HT-202", "name": "Jumeirah Creek Hotel", "city": "Dubai", "stars": 5, "price_night": 15800, "amenities": ["Pool", "Gym", "Transfer"], "rating": 4.8, "reviews_count": 892, "cancellation_policy": "Free cancellation until 72 hours before check-in", "image_url": HOTEL_IMAGES["HT-202"], "images": [HOTEL_IMAGES["HT-202"]]},
    {"id": "HT-203", "name": "Citymax Bur Dubai", "city": "Dubai", "stars": 3, "price_night": 4200, "amenities": ["WiFi", "Restaurant"], "rating": 4.1, "reviews_count": 2103, "cancellation_policy": "Non-refundable rate — no cancel", "image_url": HOTEL_IMAGES["HT-203"], "images": [HOTEL_IMAGES["HT-203"]]},
    {"id": "HT-204", "name": "Goa Palm Retreat", "city": "Goa", "stars": 4, "price_night": 6500, "amenities": ["Beach", "Pool"], "rating": 4.5, "reviews_count": 567, "cancellation_policy": "Free cancellation until 24 hours before check-in", "image_url": HOTEL_IMAGES["HT-204"], "images": [HOTEL_IMAGES["HT-204"]]},
    {"id": "HT-205", "name": "Delhi Aerocity Inn", "city": "Delhi", "stars": 4, "price_night": 5500, "amenities": ["Airport shuttle", "WiFi"], "rating": 4.3, "reviews_count": 734, "cancellation_policy": "Free cancellation until 48 hours before check-in", "image_url": HOTEL_IMAGES["HT-205"], "images": [HOTEL_IMAGES["HT-205"]]},
    {"id": "HT-206", "name": "Backpackers Hostel DXB", "city": "Dubai", "stars": 2, "price_night": 2100, "amenities": ["WiFi"], "rating": 3.8, "reviews_count": 412, "cancellation_policy": "Partial refund if cancelled 7+ days before", "image_url": HOTEL_IMAGES["HT-206"], "images": [HOTEL_IMAGES["HT-206"]]},
]

OFFERS = [
    {"code": "TRIPWISE50", "title": "5% off first booking", "discount_pct": 5},
    {"code": "FLAT2000", "title": "Rs 2000 off flights", "discount_inr": 2000},
]

TRENDING = [
    {"dest": "Dubai", "from": "DEL", "to": "DXB", "price": 18200},
    {"dest": "Goa", "from": "DEL", "to": "GOI", "price": 4500},
    {"dest": "Mumbai", "from": "DEL", "to": "BOM", "price": 5200},
]


def search_flights(from_code: str, to_code: str, passengers: int = 1, travel_class: str = "Economy") -> list:
    from_u = (from_code or "DEL").upper()[:3]
    to_u = (to_code or "DXB").upper()[:3]
    results = [
        {**f, "price_total": f["price_inr"] * passengers}
        for f in FLIGHTS_DB
        if f["from"] == from_u and f["to"] == to_u and f["class"] == travel_class
    ]
    if not results and from_u == "DEL" and to_u == "DXB":
        results = [{**f, "price_total": f["price_inr"] * passengers} for f in FLIGHTS_DB if f["to"] == "DXB"]
    return sorted(results, key=lambda x: x["price_inr"])


def search_hotels(city: str, rooms: int = 1) -> list:
    city_l = (city or "Dubai").lower()
    results = [{**h, "price_total": h["price_night"] * rooms} for h in HOTELS_DB if city_l in h["city"].lower()]
    if not results:
        results = [{**h, "price_total": h["price_night"] * rooms} for h in HOTELS_DB]
    return sorted(results, key=lambda x: x["price_night"])


def make_pnr() -> str:
    return "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6))


REFUND_MOCK = {
    "refund_id": "RF-DEMO01",
    "booking_id": "TW-2026-78421",
    "amount_inr": 89420,
    "status": "Processing",
}

def cheapest_flight(from_code: str, to_code: str, passengers: int = 1, travel_class: str = "Economy") -> dict | None:
    flights = search_flights(from_code, to_code, passengers, travel_class)
    return flights[0] if flights else None