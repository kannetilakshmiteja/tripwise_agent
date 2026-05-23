from typing import TypedDict, Optional

from langgraph.graph import StateGraph

from agents.intent_agent import detect_intent
from agents.booking_agent import get_booking_details
from agents.policy_agent import retrieve_policy
from agents.response_agent import generate_response
from agents.escalation_agent import escalation_decision


class AgentState(TypedDict):
    query: str
    booking_id: Optional[str]
    user_id: Optional[str]
    intent: str
    confidence: float
    booking: dict
    policy: str
    response: str
    escalate: bool
    reason: str


def intent_node(state):
    result = detect_intent.invoke(state["query"])
    state["intent"] = result["intent"]
    state["confidence"] = result["confidence"]
    return state


def booking_node(state):
    booking_id = state.get("booking_id") or "TW102"
    result = get_booking_details.invoke(booking_id)
    state["booking"] = result
    return state


def policy_node(state):
    result = retrieve_policy.invoke(state["intent"])
    state["policy"] = result["policy"]
    return state


def response_node(state):
    response = generate_response(
        query=state["query"],
        intent=state["intent"],
        booking=state["booking"],
        policy=state["policy"]
    )
    state["response"] = response
    return state


def escalation_node(state):
    result = escalation_decision.invoke({
        "confidence": state["confidence"]
    })

    state["escalate"] = result.get("escalate", False)
    state["reason"] = result.get("reason", "")
    return state


workflow = StateGraph(AgentState)

workflow.add_node("intent_node", intent_node)
workflow.add_node("booking_node", booking_node)
workflow.add_node("policy_node", policy_node)
workflow.add_node("response_node", response_node)
workflow.add_node("escalation_node", escalation_node)

workflow.set_entry_point("intent_node")
workflow.add_edge("intent_node", "booking_node")
workflow.add_edge("booking_node", "policy_node")
workflow.add_edge("policy_node", "response_node")
workflow.add_edge("response_node", "escalation_node")

app = workflow.compile()


def run_workflow(message: str, booking_id: str = None, user_id: str = "guest") -> dict:
    result = app.invoke({
        "query": message,
        "booking_id": booking_id,
        "user_id": user_id,
        "intent": "",
        "confidence": 0.0,
        "booking": {},
        "policy": "",
        "response": "",
        "escalate": False,
        "reason": ""
    })

    return {
        "response": result.get("response", "No response generated"),
        "intent": result.get("intent", "unknown"),
        "confidence": result.get("confidence", 0.0),
        "escalate": result.get("escalate", False),
        "agents_active": [
            "Intent Agent",
            "Booking Retrieval Agent",
            "Policy Agent",
            "Response Agent",
            "Escalation Agent"
        ],
        "sources": [
            "Mock Booking Database",
            "TripWise Policy Knowledge Base"
        ],
        "recommendations": [],
        "agents_trace": [
            {"agent": "Intent Agent", "status": "completed"},
            {"agent": "Booking Retrieval Agent", "status": "completed"},
            {"agent": "Policy Agent", "status": "completed"},
            {"agent": "Response Agent", "status": "completed"},
            {"agent": "Escalation Agent", "status": "completed"}
        ]
    }