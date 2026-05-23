from langchain.tools import tool


@tool
def detect_intent(query: str) -> dict:

    """
    Detect customer query intent.
    """

    query = query.lower()

    if "refund" in query:

        intent = "refund"

        confidence = 0.95

    elif "cancel" in query:

        intent = "cancellation"

        confidence = 0.90

    elif "booking" in query:

        intent = "booking"

        confidence = 0.90

    elif "hotel" in query:

        intent = "hotel"

        confidence = 0.88

    elif "payment" in query:

        intent = "payment"

        confidence = 0.92

    else:

        intent = "general"

        confidence = 0.60

    return {

        "intent": intent,

        "confidence": confidence
    }


if __name__ == "__main__":

    result = detect_intent.invoke(

        "Where is my refund?"
    )

    print(result)