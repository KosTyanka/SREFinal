from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .models import Concert, Order
from .schemas import ConcertCreate, TicketPurchase

def get_concerts(db: Session):
    return db.query(Concert).all()

def create_concert(db: Session, concert: ConcertCreate):
    db_concert = Concert(
        name=concert.name,
        date=concert.date,
        venue=concert.venue,
        total_tickets=concert.total_tickets,
        tickets_remaining=concert.total_tickets
    )
    db.add(db_concert)
    db.commit()
    db.refresh(db_concert)
    return db_concert

def process_ticket_purchase(db: Session, purchase: TicketPurchase):
    # Lock the concert row for update to prevent race conditions
    concert = db.query(Concert).with_for_update().filter(
        Concert.id == purchase.concert_id
    ).first()
    
    if not concert:
        raise HTTPException(status_code=404, detail="Concert not found")
    
    if concert.tickets_remaining < purchase.quantity:
        raise HTTPException(status_code=400, detail="Not enough tickets available")
    
    # Update tickets atomically
    concert.tickets_remaining -= purchase.quantity
    
    # Create order
    order = Order(
        concert_id=purchase.concert_id,
        quantity=purchase.quantity
    )
    db.add(order)
    
    try:
        db.commit()
        db.refresh(order)
        return {
            "order_id": order.id,
            "tickets_purchased": purchase.quantity,
            "tickets_remaining": concert.tickets_remaining
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to process purchase") 