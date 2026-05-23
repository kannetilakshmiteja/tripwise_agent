from fastapi import APIRouter
from schemas import ChatRequest
from services.chat_service import process_chat

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    return process_chat(request)