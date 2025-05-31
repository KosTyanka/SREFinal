from pydantic import BaseModel, conint
from datetime import datetime

class ConcertBase(BaseModel):
    name: str
    date: datetime
    venue: str
    total_tickets: conint(gt=0)

class ConcertCreate(ConcertBase):
    pass

class ConcertResponse(ConcertBase):
    id: int
    tickets_remaining: int
    created_at: datetime

    class Config:
        from_attributes = True

class TicketPurchase(BaseModel):
    concert_id: int
    quantity: conint(gt=0, le=100)  # Maximum 100 tickets per purchase

class OrderResponse(BaseModel):
    id: int
    concert_id: int
    quantity: int
    purchase_time: datetime

    class Config:
        from_attributes = True 