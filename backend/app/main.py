from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response, JSONResponse
import time
import os
from datetime import datetime
from prometheus_fastapi_instrumentator import Instrumentator

# Database setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Concert(Base):
    __tablename__ = "concerts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime)
    venue = Column(String)
    available_tickets = Column(Integer)
    price = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Prometheus metrics
tickets_sold = Counter('tickets_sold_total', 'Total number of tickets sold')
available_tickets = Gauge('available_tickets', 'Current number of available tickets')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration in seconds')

# Initialize Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize sample data
def init_db():
    db = SessionLocal()
    try:
        # Check if we already have concerts
        if db.query(Concert).first() is None:
            sample_concerts = [
                Concert(
                    name="Jennifer Lopez - Astana Kazakhstan",
                    date=datetime(2024, 6, 15),
                    venue="Astana Arena",
                    available_tickets=100,
                    price=49.99
                ),
                Concert(
                    name="Imagine Dragons - Kazakhstan",
                    date=datetime(2024, 7, 1),
                    venue="Central Stadium Almaty",
                    available_tickets=50,
                    price=29.99
                ),
                Concert(
                    name="Coldplay - Kazakhstan",
                    date=datetime(2024, 7, 15),
                    venue="Almaty Arena",
                    available_tickets=200,
                    price=39.99
                )
            ]
            for concert in sample_concerts:
                db.add(concert)
            db.commit()

            # Initialize Prometheus metrics with total available tickets
            total_tickets = sum(concert.available_tickets for concert in sample_concerts)
            available_tickets.set(total_tickets)
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()

# Initialize database with sample data
init_db()

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    request_duration.observe(process_time)
    return response

@app.get("/api/concerts")
def get_concerts():
    db = SessionLocal()
    try:
        concerts = db.query(Concert).all()
        # Update available tickets metric
        total_tickets = sum(concert.available_tickets for concert in concerts)
        available_tickets.set(total_tickets)
        
        return JSONResponse(content=[
            {
                "id": concert.id,
                "name": concert.name,
                "date": concert.date.isoformat(),
                "venue": concert.venue,
                "available_tickets": concert.available_tickets,
                "price": concert.price
            }
            for concert in concerts
        ])
    except Exception as e:
        print(f"Error getting concerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/api/concerts/{concert_id}/tickets")
async def buy_ticket(concert_id: int):
    db = SessionLocal()
    try:
        concert = db.query(Concert).filter(Concert.id == concert_id).first()
        if not concert:
            return JSONResponse(
                status_code=404,
                content={"detail": "Concert not found"}
            )
        if concert.available_tickets <= 0:
            return JSONResponse(
                status_code=400,
                content={"detail": "No tickets available"}
            )
        
        concert.available_tickets -= 1
        db.commit()
        
        # Update Prometheus metrics
        tickets_sold.inc()
        available_tickets.dec()  # Now using Gauge which has dec() method
        
        return JSONResponse(
            content={"message": "Ticket purchased successfully"}
        )
    except Exception as e:
        print(f"Error purchasing ticket: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy"} 