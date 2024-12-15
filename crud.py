from sqlalchemy import select
from datetime import datetime

from typing import Annotated
from db import async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

SessAsync = Annotated[AsyncSession, Depends(async_session)]

def date_format(data: dict) -> dict:
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