from sqlalchemy import select
from datetime import datetime

from typing import Annotated, Optional
from db import async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

SessAsync = Annotated[AsyncSession, Depends(async_session)]

def date_format(data: dict) -> dict:
    if data["deadline"]:
        data["deadline"] = datetime.strptime(data["deadline"],"%Y-%m-%d").isoformat()
    return data
    

async def add_db(ORMmodel,data: dict,session: SessAsync):
    save = ORMmodel(**data)
    session.add(save)
    await session.commit()
    return save


async def in_db_id(ORMmodel,data: int,session: SessAsync):
    adv = select(ORMmodel).where(ORMmodel.id == data)
    result = await session.execute(adv)
    user = result.scalars().first()
    return user

async def get_todos_from_db(
    ORMmodel,
    tags: Optional[str],
    status: Optional[bool],
    sort_by: str,
    page: int,
    page_size: int,
    session: AsyncSession):
    query = select(ORMmodel)
    if tags:
        query = query.where(ORMmodel.tags.like(f"%{tags}%"))
    if status is not None:
        query = query.where(ORMmodel.status == status)
    if sort_by in ["deadline", "create_datetime", "title"]:
        query = query.order_by(getattr(ORMmodel, sort_by))

    skip = (page - 1) * page_size
    query = query.offset(skip).limit(page_size)
    result = await session.execute(query)
    todos = result.scalars().all()
    
    return todos