from schemas import ChatRequest
from orchestrator.workflow import run_workflow


def process_chat(request: ChatRequest):
    return run_workflow(
        message=request.message,
        booking_id=request.booking_id,
        user_id=request.user_id
    )