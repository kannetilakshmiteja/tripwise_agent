from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router
from database import init_db
from routes.auth import router as auth_router

app = FastAPI(
    title="TripWise Backend"
)
init_db()
# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "TripWise backend running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
@app.get("/bookings/me")
def get_my_bookings():
    return {
        "bookings": [
            {
                "booking_id": "TW12345",
                "destination": "Dubai",
                "status": "Confirmed"
            }
        ]
    }