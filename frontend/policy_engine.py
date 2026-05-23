"""Refund/cancellation policy — demo calculations; live uses Person 2 API."""
from datetime import datetime, timezone


def calc_refund(booking: dict, preview: bool = True) -> dict:
    btype = booking.get("type", "flight")
    amount = int(booking.get("amount_inr", 0))
    fare = booking.get("fare_type") or booking.get("flight", {}).get("fare_type", "Refundable")
    policy = booking.get("cancellation_policy", "")
    flight_status = booking.get("flight_status", "OnTime")
    insurance = booking.get("insurance", False)
    fee = 0
    refund = 0
    policy_text = ""

    if btype == "hotel":
        if "Free cancellation" in policy or "free cancel" in policy.lower():
            fee = int(amount * 0.1) if "48" not in policy else 0
            refund = max(0, amount - fee)
            policy_text = policy
        elif "Non-refundable" in policy:
            fee = amount
            refund = 0
            policy_text = "Non-refundable hotel rate"
        else:
            fee = int(amount * 0.2)
            refund = amount - fee
            policy_text = policy or "Partial refund per hotel policy"
    else:
        if flight_status == "Cancelled":
            refund = amount
            policy_text = "Full refund — flight cancelled by airline"
        elif flight_status == "Delayed" and booking.get("delay_minutes", 0) >= 180:
            refund = amount if insurance else int(amount * 0.9)
            policy_text = "Refund eligible due to major delay"
        elif fare == "Non-refundable":
            fee = int(amount * 0.85)
            refund = max(0, amount - fee)
            policy_text = "Non-refundable fare — airline fee applies"
        elif fare == "Partial":
            fee = int(amount * 0.35)
            refund = amount - fee
            policy_text = "Partially refundable fare"
        else:
            fee = int(amount * 0.15)
            refund = amount - fee
            policy_text = "Refundable fare — standard cancellation fee"

    timeline = [
        {"step": "Cancellation requested", "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "done": True},
        {"step": "Processing refund", "date": "3-5 business days", "done": preview},
        {"step": "Credited to payment method", "date": "5-7 business days", "done": False},
    ]
    return {
        "refund_eligible_inr": refund,
        "cancellation_fee_inr": fee,
        "policy_text": policy_text,
        "timeline": timeline,
    }
