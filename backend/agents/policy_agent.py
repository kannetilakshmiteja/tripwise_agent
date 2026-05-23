from langchain.tools import tool


POLICIES = {

    "refund":
    "Refunds are processed within 7 working days.",

    "cancellation":
    "Flight cancellation within 24 hours receives 80% refund.",

    "hotel":
    "Hotel cancellation allowed before 48 hours.",

    "payment":
    "Payment verification may take up to 30 minutes."
}


@tool
def retrieve_policy(intent: str) -> dict:

    """
    Retrieve travel policy information.
    """

    policy = POLICIES.get(

        intent,

        "No matching policy found."
    )

    return {

        "intent": intent,

        "policy": policy,

        "source": "TripWise Policy Knowledge Base"
    }


if __name__ == "__main__":

    result = retrieve_policy.invoke("refund")

    print(result)