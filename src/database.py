from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
import settings as settings

engine = create_engine(
    url=settings.SYNC_DATABASE_URL,
    echo=True,  # log all the queries in console
    pool_size=5,  # max connections to db
    max_overflow=10,  # 10 more connections if 5 are taken
)



