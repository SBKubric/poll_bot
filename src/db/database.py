from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from core.config import settings

SQLALCHEMY_DATABASE_URL = settings.db_url

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()
