# TripWise — Person 1 Streamlit Frontend

MakeMyTrip-style **Agentic AI Travel** platform. Person 1 owns **frontend/** only; Person 2 owns **backend/**.

## Run (demo mode — no backend)

```powershell
cd C:\Users\tnikhila001\tripwise-capstone\frontend
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

## Run with Person 2

```powershell
# Terminal 1 — Person 2
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 — Person 1
cd frontend
$env:TRIPWISE_API_URL="http://127.0.0.1:8000"
streamlit run app.py
```

Navbar shows **Backend Connected** or **Demo Mode**.

## First visit

1. **Login** — mobile OTP (demo OTP: **123456**), one-time profile
2. **Home** — search flights/hotels, offers, trending
3. **Flights** — tabs: Search → Results → Payment & Book → Confirmation
4. **Hotels** — images, ratings, same tab flow
5. **AI Support** — chat with 20-agent trace
6. **My Trips** — cancel with refund preview, flight status
7. **Refunds** — timeline with hotel thumbnails
8. **Agents** — full catalog

## Integration

All server calls go through **`api_client.py`** only. Contract for Person 2: **`INTEGRATION.md`**.

Demo OTP: `123456` for any 10-digit mobile when API is offline.

## Branch

`person1-frontend` — commit only `frontend/`
