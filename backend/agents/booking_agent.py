from langchain.tools import tool
from typing import Dict


# ==========================================
# MOCK BOOKING DATABASE
# ==========================================

BOOKINGS_DB = {

    "TW101": {

        "booking_id": "TW101",

        "customer_name": "Rahul Sharma",

        "travel_type": "Flight",

        "flight": "Delhi → Dubai",

        "airline": "IndiGo",

        "travel_date": "2025-12-15",

        "booking_status": "Confirmed",

        "payment_status": "Paid",

        "refund_status": "Not Requested"
    },

    "TW102": {

        "booking_id": "TW102",

        "customer_name": "Ananya Rao",

        "travel_type": "Flight",

        "flight": "Mumbai → Singapore",

        "airline": "Air India",

        "travel_date": "2025-12-20",

        "booking_status": "Cancelled",

        "payment_status": "Paid",

        "refund_status": "Processing"
    },

    "TW103": {

        "booking_id": "TW103",

        "customer_name": "Amit Verma",

        "travel_type": "Hotel",

        "hotel_name": "Palm Residency Dubai",

        "check_in": "2025-12-25",

        "booking_status": "Confirmed",

        "payment_status": "Paid",

        "refund_status": "Not Applicable"
    }
}


# ==========================================
# BOOKING RETRIEVAL TOOL
# ==========================================

@tool
def get_booking_details(booking_id: str) -> Dict:

    """
    Retrieve booking details using booking ID.
    Used by the Booking Retrieval Agent.
    """

    booking = BOOKINGS_DB.get(booking_id)

    # BOOKING FOUND
    if booking:

        return {

            "success": True,

            "confidence": 0.95,

            "source": "Mock Booking Database",

            "data": booking
        }

    # BOOKING NOT FOUND
    return {

        "success": False,

        "confidence": 0.40,

        "source": "Mock Booking Database",

        "error": f"No booking found for ID: {booking_id}"
    }


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    result = get_booking_details.invoke("TW102")

    print("\nBOOKING RETRIEVAL RESULT:\n")

    print(result)