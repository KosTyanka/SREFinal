from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/ticketing")
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Concert(Base):
    __tablename__ = "concerts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime)
    venue = Column(String)
    total_tickets = Column(Integer)
    tickets_remaining = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="concert")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    concert_id = Column(Integer, ForeignKey("concerts.id"))
    quantity = Column(Integer)
    purchase_time = Column(DateTime, default=datetime.utcnow)
    concert = relationship("Concert", back_populates="orders") 