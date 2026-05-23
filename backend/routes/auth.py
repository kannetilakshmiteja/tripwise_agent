import hashlib
from fastapi import APIRouter, HTTPException
from schemas import RegisterRequest, LoginRequest
from database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/register")
def register_user(request: RegisterRequest):
    conn = get_db()

    existing = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (request.email,)
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    conn.execute(
        """
        INSERT INTO users (full_name, email, mobile, password_hash)
        VALUES (?, ?, ?, ?)
        """,
        (
            request.full_name,
            request.email,
            request.mobile,
            hash_password(request.password)
        )
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Registration successful"
    }


@router.post("/login")
def login_user(request: LoginRequest):
    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (request.email,)
    ).fetchone()

    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user["password_hash"] != hash_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "user_id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "mobile": user["mobile"]
        }
    }