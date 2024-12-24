import os

import datetime

from sqlalchemy import MetaData, Integer, String, Boolean, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER',"postgres")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD',"0596")
POSTGRES_DB = os.getenv('POSTGRES_DB',"postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST","5432")

DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_HOST}/{POSTGRES_DB}"
engine = create_async_engine(DSN) 

Base = declarative_base(metadata=MetaData())

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Todo(Base):
    __tablename__ = "todo"
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    deadline: Mapped[datetime.date] = mapped_column(Date,nullable=True)
    tags: Mapped[str] = mapped_column(String,nullable=True)
    status: Mapped[bool] = mapped_column(Boolean,default=False)
    create_datetime: Mapped[datetime.datetime] =  mapped_column(DateTime,server_default=func.now())

    def dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "tags": self.tags,
            "status": self.status,
            "create_datetime": self.create_datetime
            }



async def async_session():
    async with async_session_maker() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)