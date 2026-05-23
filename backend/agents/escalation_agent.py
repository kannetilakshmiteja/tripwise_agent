from langchain.tools import tool


@tool
def escalation_decision(confidence: float) -> dict:

    """
    Determine whether query
    requires human escalation.
    """

    if confidence < 0.75:

        return {

            "escalate": True,

            "reason": "Low confidence response"
        }

    return {

        "escalate": False,

        "reason": "No escalation required"
    }


if __name__ == "__main__":

    result = escalation_decision.invoke(0.60)

    print(result)