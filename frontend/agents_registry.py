"""All 20 TripWise AI agents — single source of truth."""

AGENT_CATEGORIES = ["All", "Booking", "Refund & Cancel", "Disruption", "Hotel", "Flight", "Policy", "Payment", "General"]

AGENT_CATEGORY_MAP = {
    "intent": "General",
    "booking_status": "Booking",
    "booking_retrieval": "Booking",
    "flight_search": "Flight",
    "hotel_search": "Hotel",
    "payment": "Payment",
    "refund": "Refund & Cancel",
    "cancellation": "Refund & Cancel",
    "baggage": "Policy",
    "hotel_policy": "Hotel",
    "package": "Booking",
    "disruption": "Disruption",
    "rebooking": "Disruption",
    "alt_stay": "Hotel",
    "itinerary": "Booking",
    "travel_advisory": "Policy",
    "policy": "Policy",
    "recommendation": "General",
    "response": "General",
    "escalation": "General",
}

AGENTS = [
    {"id": "intent", "name": "Intent Classification", "icon": "🎯", "desc": "Routes queries to the right specialist agent", "category": "General"},
    {"id": "booking_status", "name": "Booking Status", "icon": "📋", "desc": "Flight/hotel booking status, PNR, confirmed or pending", "category": "Booking"},
    {"id": "booking_retrieval", "name": "Booking Retrieval", "icon": "📂", "desc": "Passengers, itinerary, add-ons, full booking record", "category": "Booking"},
    {"id": "flight_search", "name": "Flight Search & Booking", "icon": "✈", "desc": "Search flights, lowest fare, compare, book", "category": "Flight"},
    {"id": "hotel_search", "name": "Hotel Search & Booking", "icon": "🏨", "desc": "Search hotels, availability, book stays", "category": "Hotel"},
    {"id": "payment", "name": "Payment Status", "icon": "💳", "desc": "Payment confirmation, receipts, transaction status", "category": "Payment"},
    {"id": "refund", "name": "Refund Tracking", "icon": "💰", "desc": "Refund amount, timeline, why not credited", "category": "Refund & Cancel"},
    {"id": "cancellation", "name": "Cancellation & Charges", "icon": "❌", "desc": "Cancel bookings, fees, refund estimates", "category": "Refund & Cancel"},
    {"id": "baggage", "name": "Baggage Policy", "icon": "🧳", "desc": "Airline baggage allowance by fare type", "category": "Policy"},
    {"id": "hotel_policy", "name": "Hotel Policy", "icon": "🛎", "desc": "Check-in/out, ID rules, overbooking policy", "category": "Hotel"},
    {"id": "package", "name": "Package Support", "icon": "🎒", "desc": "Holiday package inclusions and legs", "category": "Booking"},
    {"id": "disruption", "name": "Disruption Handling", "icon": "⚡", "desc": "Delays, cancellations, weather, missed connections", "category": "Disruption"},
    {"id": "rebooking", "name": "Rebooking", "icon": "🔄", "desc": "Alternate flights, same-day rebook, fee waivers", "category": "Disruption"},
    {"id": "alt_stay", "name": "Alternate Accommodation", "icon": "🏠", "desc": "Hotel swap when overbooked or stranded", "category": "Hotel"},
    {"id": "itinerary", "name": "Itinerary Modification", "icon": "🗺", "desc": "Change dates, legs, modify before departure", "category": "Booking"},
    {"id": "travel_advisory", "name": "Travel Advisory", "icon": "🌍", "desc": "Visa hints, travel advisories, documents", "category": "Policy"},
    {"id": "policy", "name": "Policy & Rules (RAG)", "icon": "📜", "desc": "Airline, hotel, fare, refund rules from knowledge base", "category": "Policy"},
    {"id": "recommendation", "name": "Recommendation", "icon": "💡", "desc": "Cheapest options, add-ons, insurance, packages", "category": "General"},
    {"id": "response", "name": "Response Generation", "icon": "💬", "desc": "Clear customer-friendly grounded answer", "category": "General"},
    {"id": "escalation", "name": "Escalation", "icon": "🚨", "desc": "Human handoff for disputes and low confidence", "category": "General"},
]

AGENT_BY_ID = {a["id"]: a for a in AGENTS}
AGENT_BY_NAME = {a["name"]: a for a in AGENTS}

INTENT_AGENT_CHAINS = {
    "booking_status": ["intent", "booking_status", "booking_retrieval", "policy", "recommendation", "response", "escalation"],
    "booking": ["intent", "booking_status", "booking_retrieval", "policy", "recommendation", "response", "escalation"],
    "refund": ["intent", "refund", "payment", "policy", "booking_retrieval", "response", "escalation"],
    "cancellation": ["intent", "cancellation", "refund", "hotel_policy", "policy", "booking_retrieval", "response", "escalation"],
    "delay": ["intent", "disruption", "rebooking", "recommendation", "flight_search", "policy", "response", "escalation"],
    "disruption": ["intent", "disruption", "rebooking", "recommendation", "response", "escalation"],
    "hotel_issue": ["intent", "hotel_policy", "alt_stay", "hotel_search", "recommendation", "response", "escalation"],
    "hotel_booking": ["intent", "hotel_search", "hotel_policy", "recommendation", "response", "escalation"],
    "payment": ["intent", "payment", "booking_retrieval", "response", "escalation"],
    "baggage": ["intent", "baggage", "policy", "response", "escalation"],
    "itinerary": ["intent", "itinerary", "package", "travel_advisory", "policy", "response", "escalation"],
    "package": ["intent", "package", "itinerary", "policy", "response", "escalation"],
    "flight_booking": ["intent", "flight_search", "recommendation", "policy", "response", "escalation"],
    "lowest_fare": ["intent", "flight_search", "recommendation", "response", "escalation"],
    "travel_advisory": ["intent", "travel_advisory", "policy", "response", "escalation"],
    "general_support": ["intent", "policy", "booking_retrieval", "recommendation", "response", "escalation"],
}

SAMPLE_QUERIES_BY_CATEGORY = {
    "Booking": [
        "What is the status of my Delhi to Dubai flight booking?",
        "Show my booking TW-2026-78421 details",
    ],
    "Refund & Cancel": [
        "I want to cancel my hotel booking and know the refund amount.",
        "Why has my refund not been credited yet?",
    ],
    "Disruption": [
        "My flight is delayed — what are my alternate travel options?",
    ],
    "Hotel": [
        "What is the check-in policy for Marina Bay Resort?",
        "Hotel overbooking — need alternate accommodation",
    ],
    "Flight": [
        "Find the cheapest flight from Delhi to Dubai on 14 June",
        "Book lowest fare DEL to Dubai",
    ],
    "Policy": [
        "What are the baggage rules for Emirates Economy Saver?",
        "Help me modify my holiday package itinerary before departure.",
    ],
    "Payment": [
        "Was my payment successful for booking TW-2026-78421?",
    ],
    "Escalation": [
        "I dispute this cancellation and want a human agent.",
    ],
}

AGENT_SAMPLE_QUERIES = {
    "booking_status": "What is the status of my Delhi to Dubai flight booking?",
    "refund": "Why has my refund not been credited yet?",
    "cancellation": "Cancel my hotel and tell me the refund amount",
    "disruption": "My flight is delayed — alternate options?",
    "flight_search": "Find cheapest DEL to Dubai flights",
    "baggage": "Baggage rules for my airline and ticket type",
    "itinerary": "Modify my holiday package before departure",
    "payment": "Payment status for my booking",
}
