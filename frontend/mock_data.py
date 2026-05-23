"""Mock chat responses with 20-agent routing."""
import random
from datetime import datetime, timezone

from agents_registry import AGENT_BY_ID, INTENT_AGENT_CHAINS
from mock_inventory import REFUND_MOCK, cheapest_flight, search_flights

AGENT_DETAILS = {
    "intent": lambda intent, _: f"Detected intent: {intent.replace('_', ' ')}",
    "booking_status": lambda _, __: "Booking TW-2026-78421 status: Confirmed",
    "booking_retrieval": lambda _, __: "Loaded itinerary, passengers, payment Paid",
    "flight_search": lambda intent, msg: _flight_detail(intent, msg),
    "hotel_search": lambda _, __: "Queried hotel inventory for Dubai",
    "payment": lambda _, __: "Payment PAY-44102: Successful ₹89,420",
    "refund": lambda _, __: f"Refund {REFUND_MOCK['refund_id']}: {REFUND_MOCK['status']}",
    "cancellation": lambda _, __: "Cancellation fees applied per fare rules",
    "baggage": lambda _, __: "Emirates Economy: 25kg check-in, 7kg cabin",
    "hotel_policy": lambda _, __: "Check-in 14:00, ID required, free cancel 48h prior",
    "package": lambda _, __: "Package TW-PKG-992: flight + 3N hotel + safari",
    "disruption": lambda intent, _: "Urgency HIGH — delay 4h on EK-513" if intent == "delay" else "Monitoring disruptions",
    "rebooking": lambda intent, _: "2 alternate flights available same day" if intent == "delay" else "No rebook needed",
    "alt_stay": lambda intent, _: "Jumeirah Creek available" if intent == "hotel_issue" else "Skipped",
    "itinerary": lambda _, __: "Changes allowed up to 72h before departure",
    "travel_advisory": lambda _, __: "UAE visa on arrival for Indian passport (check validity)",
    "policy": lambda _, __: "Matched 3 clauses from policies.txt / Chroma RAG",
    "recommendation": lambda intent, msg: _recommend_detail(intent, msg),
    "response": lambda _, __: "Generated grounded customer-friendly answer",
    "escalation": lambda conf, _: "Human agent recommended" if conf < 0.6 else "Auto-resolve OK",
}


def _flight_detail(intent: str, msg: str) -> str:
    if intent in ("lowest_fare", "flight_booking"):
        c = cheapest_flight("DEL", "DXB")
        if c:
            return f"Lowest: {c['airline']} {c['flight_no']} ₹{c['price_inr']:,}"
    return "Searched flight inventory"


def _recommend_detail(intent: str, msg: str) -> str:
    if intent in ("lowest_fare", "flight_booking", "delay"):
        return "Top 3 options ranked by price and duration"
    return "Generated next-best actions"


def _detect_intent(message: str) -> str:
    m = message.lower()
    if any(w in m for w in ("cheapest", "lowest", "cheap")):
        return "lowest_fare"
    if any(w in m for w in ("book flight", "book a flight", "search flight")):
        return "flight_booking"
    if any(w in m for w in ("book hotel", "search hotel")):
        return "hotel_booking"
    if any(w in m for w in ("refund", "credited", "money back")):
        return "refund"
    if any(w in m for w in ("cancel", "cancellation")):
        return "cancellation"
    if any(w in m for w in ("delay", "disruption", "missed", "alternate")):
        return "delay"
    if any(w in m for w in ("overbook", "check-in", "check in")):
        return "hotel_issue"
    if "hotel" in m:
        return "hotel_booking" if any(w in m for w in ("book", "search", "find")) else "hotel_issue"
    if any(w in m for w in ("payment", "paid", "transaction", "receipt")):
        return "payment"
    if any(w in m for w in ("baggage", "luggage", "kg")):
        return "baggage"
    if any(w in m for w in ("visa", "advisory", "document")):
        return "travel_advisory"
    if any(w in m for w in ("package", "safari", "inclusion")):
        return "package"
    if any(w in m for w in ("modify", "itinerary", "change leg")):
        return "itinerary"
    if any(w in m for w in ("dispute", "lawyer", "human agent")):
        return "cancellation"
    if any(w in m for w in ("status", "pnr", "dubai", "delhi")) and any(w in m for w in ("booking", "flight", "status")):
        return "booking_status"
    if any(w in m for w in ("booking", "flight")):
        return "booking_status"
    return "general_support"


def _booking_summary(intent: str) -> dict:
    return {
        "booking_id": "TW-2026-78421",
        "customer_name": "Priya Sharma",
        "route": "Delhi (DEL) → Dubai (DXB)",
        "flight": "Emirates EK-513",
        "departure": "2026-06-14 02:35 IST",
        "hotel": "Marina Bay Resort, Dubai — 3 nights",
        "status": "Confirmed" if intent != "cancellation" else "Cancellation requested",
        "payment_status": "Paid",
        "amount_inr": 89420,
        "pnr": "X7K9PQ",
    }


def _recommendations(intent: str, message: str) -> list:
    if intent in ("lowest_fare", "flight_booking"):
        flights = search_flights("DEL", "DXB")[:3]
        return [{"type": "flight", "title": f"{f['airline']} {f['flight_no']} — ₹{f['price_inr']:,}", "detail": f"{f['dep']} · {f['stops']} stops"} for f in flights]
    if intent == "delay":
        return [
            {"type": "flight", "title": "Emirates EK-515 — dep 08:40", "detail": "Same day, 2 seats"},
            {"type": "flight", "title": "Air India AI-996 — dep 11:20", "detail": "Lower fare"},
            {"type": "refund", "title": "Full refund eligible", "detail": "Policy DOC-12"},
        ]
    if intent in ("cancellation", "refund"):
        return [
            {"type": "refund", "title": "Estimated refund ₹62,400", "detail": "After fees"},
            {"type": "policy", "title": "5–7 business days", "detail": "Original payment mode"},
        ]
    if intent == "hotel_issue":
        return [{"type": "hotel", "title": "Jumeirah Creek Hotel", "detail": "Partner rate + transfer"}]
    return [
        {"type": "addon", "title": "Travel insurance ₹499", "detail": "Covers disruption"},
        {"type": "addon", "title": "Airport lounge DEL T3", "detail": "₹1,200"},
    ]


def _build_agent_trace(intent: str, confidence: float, message: str) -> tuple[list, list]:
    chain = INTENT_AGENT_CHAINS.get(intent, INTENT_AGENT_CHAINS["general_support"])
    trace = []
    for aid in chain:
        agent = AGENT_BY_ID.get(aid, {"name": aid})
        name = agent["name"]
        if aid == "escalation":
            status = "triggered" if confidence < 0.6 else "completed"
        elif aid in ("alt_stay", "rebooking") and intent not in ("delay", "hotel_issue"):
            status = "skipped"
        else:
            status = "completed"
        fn = AGENT_DETAILS.get(aid, lambda *_: "Done")
        detail = fn(intent if aid != "escalation" else confidence, message)
        trace.append({"agent": name, "status": status, "detail": detail, "id": aid})
    return trace, chain


def _build_response(message: str, intent: str) -> str:
    responses = {
        "booking_status": (
            "Your Delhi → Dubai booking **TW-2026-78421** is **Confirmed**. "
            "Flight **Emirates EK-513** departs **14 Jun 2026, 02:35 IST**. PNR **X7K9PQ**. "
            "Hotel **Marina Bay Resort** 3 nights. Payment: **Paid** (₹89,420)."
        ),
        "refund": (
            f"Refund **{REFUND_MOCK['refund_id']}** for TW-2026-78421 is **{REFUND_MOCK['status']}**. "
            f"Estimated **₹{REFUND_MOCK['amount_inr']:,}** credited by **20 May 2026**."
        ),
        "cancellation": (
            "Cancellation for **TW-2026-78421**: estimated refund **₹62,400** after fee **₹12,000**. "
            "Hotel: free cancel if 48h+ before check-in."
        ),
        "delay": (
            "**Disruption — EK-513 delayed ~4h.** Rebook **EK-515 (08:40)** or **AI-996 (11:20)** free, "
            "or full refund per **DOC-12**."
        ),
        "hotel_issue": (
            "Hotel issue logged for **Marina Bay Resort**. Alternate: **Jumeirah Creek** at partner rate."
        ),
        "hotel_booking": (
            "Found hotels in Dubai from **₹2,100/night**. Best value: **Citymax Bur Dubai**. "
            "Use the **Hotels** page to book."
        ),
        "payment": (
            "Payment **Successful** — ₹89,420 via UPI. Receipt **PAY-44102** on 02 May 2026."
        ),
        "baggage": (
            "**Emirates Economy Saver:** 25 kg checked, 7 kg cabin. Extra 5 kg: ₹2,200 online."
        ),
        "itinerary": (
            "Package **TW-PKG-992**: modify up to **72h** before departure. Legs: flight + hotel + safari."
        ),
        "package": (
            "Package includes: DEL→DXB flight, 3N Marina Bay, desert safari, airport transfer."
        ),
        "flight_booking": (
            "Use **Flights** page or I can search — say route and date. Lowest DEL→DXB from **₹18,200**."
        ),
        "lowest_fare": (
            _lowest_fare_text()
        ),
        "travel_advisory": (
            "Indian passport: UAE visa on arrival (14 days). Ensure passport 6+ months valid. "
            "Travel insurance recommended."
        ),
        "general_support": (
            f"Thanks for contacting TripWise. For booking **TW-2026-78421** support, "
            "ask about status, refund, baggage, or delays."
        ),
    }
    return responses.get(intent, responses["general_support"])


def _lowest_fare_text() -> str:
    c = cheapest_flight("DEL", "DXB")
    if not c:
        return "No flights found for DEL→DXB."
    return (
        f"**Lowest fare DEL → DXB:** **{c['airline']} {c['flight_no']}** at **₹{c['price_inr']:,}** "
        f"({c['dep']} · {'Non-stop' if c['stops']==0 else str(c['stops'])+' stop'}). Book on the Flights page."
    )


def generate_mock_chat_response(message: str) -> dict:
    intent = _detect_intent(message)
    confidence = round(random.uniform(0.72, 0.96), 2)
    if any(w in message.lower() for w in ("dispute", "lawyer", "human agent")):
        confidence = round(random.uniform(0.35, 0.55), 2)
    escalate = confidence < 0.6
    trace, active = _build_agent_trace(intent, confidence, message)
    flight_options = []
    if intent in ("lowest_fare", "flight_booking", "delay"):
        flight_options = search_flights("DEL", "DXB")[:5]
    return {
        "response": _build_response(message, intent),
        "confidence": confidence,
        "intent": intent,
        "escalate": escalate,
        "escalation_reason": "Low confidence or disputed case — human agent recommended" if escalate else "",
        "booking_summary": _booking_summary(intent),
        "recommendations": _recommendations(intent, message),
        "agents_trace": trace,
        "agents_active": active,
        "flight_options": flight_options,
        "sources": ["bookings.db", "policies.txt", "refunds.csv", "mock_inventory"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "mock",
    }
