from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from .models import engine

# Configure session with connection pooling
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    # Configure pool size based on expected concurrent connections
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 