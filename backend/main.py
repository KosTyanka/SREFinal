from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge

class TicketBooking(BaseModel):
    concert_id: int
    quantity: int
    user_email: str

class Concert(BaseModel):
    id: int
    name: str
    venue: str
    location: str
    available_tickets: int

# Initialize Prometheus metrics
ACTIVE_TICKETS = Gauge('active_tickets', 'Number of active tickets')
HTTP_REQUESTS_TOTAL = Counter('http_requests_total', 'Total HTTP requests')

app = FastAPI()

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    HTTP_REQUESTS_TOTAL.inc()
    return {"message": "Welcome to Concert Ticketing API"}

@app.get("/health")
async def health_check():
    HTTP_REQUESTS_TOTAL.inc()
    return {"status": "healthy"}

@app.get("/concerts", response_model=List[Concert])
async def get_concerts():
    try:
        HTTP_REQUESTS_TOTAL.inc()
        concerts = [
            {
                "id": 1,
                "name": "Jennifer Lopez",
                "venue": "Astana Arena",
                "location": "Astana Kazakhstan",
                "available_tickets": 100
            },
            {
                "id": 2,
                "name": "Imagine Dragons",
                "venue": "Central Stadium",
                "location": "Almaty Kazakhstan",
                "available_tickets": 150
            },
            {
                "id": 3,
                "name": "Coldplay",
                "venue": "Almaty Arena",
                "location": "Kazakhstan",
                "available_tickets": 200
            }
        ]
        # Update active tickets metric
        total_tickets = sum(concert["available_tickets"] for concert in concerts)
        ACTIVE_TICKETS.set(total_tickets)
        return concerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book-ticket", response_model=Dict[str, str])
async def book_ticket(booking: TicketBooking):
    try:
        HTTP_REQUESTS_TOTAL.inc()
        # Simulate ticket booking
        ACTIVE_TICKETS.dec(booking.quantity)
        return {
            "status": "success",
            "message": f"Booked {booking.quantity} ticket(s) for concert {booking.concert_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 