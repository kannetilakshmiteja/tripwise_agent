from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from pydantic import EmailStr


class ChatRequest(BaseModel):
    message: str
    booking_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = "guest"


class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    escalate: bool = False
    agents_active: Optional[List[str]] = []
    sources: Optional[List[str]] = []
    recommendations: Optional[List[str]] = []
    agents_trace: Optional[List[Dict[str, Any]]] = []



class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    mobile: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str