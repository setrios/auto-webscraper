from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import settings



engine = create_engine(
    url=settings.SYNC_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()