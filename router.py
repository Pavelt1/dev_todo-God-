from typing import Optional
from fastapi import APIRouter, HTTPException

from db import Todo
from schema import TodoRequest, TodoResponse, TodoUpdate
from crud import SessAsync, add_db, date_format, get_todos_from_db, in_db_id

router = APIRouter(
    prefix="/todo",
    tags = ["todo"]
)

@router.post("/create/")
async def create_todo(jsonData: TodoRequest,session: SessAsync):
    data = jsonData.dict()
    new = await add_db(Todo,date_format(data),session)
    return new


@router.patch("/update/{id}")
async def update_todo(id: int,jsonData: TodoUpdate,session: SessAsync):
    data = jsonData.dict()
    response = await in_db_id(Todo,id,session)
    if response:
        for key,value in (date_format(data)).items():
            setattr(response, key, value)
        await session.commit()
        return {f"Todo {id}":" updated"}
    else:
        raise HTTPException(status_code=404,detail="Not found")
        


@router.delete("/delete/{id}")
async def delete_todo(id: int,session: SessAsync):
    response = await in_db_id(Todo,id,session)
    if response:
        await session.delete(response)
        await session.commit()
        return {f"Todo {id}":" deleted"}
    else:
        raise HTTPException(status_code=404,detail="Not found")
    

@router.patch("/status_ok/{id}")
async def update_status(id: int,status: bool,session: SessAsync):
    response = await in_db_id(Todo,id,session)
    if response:
        response.status = status
        await session.commit()
        return {f"Todo {id}":" updated"}
    else:
        raise HTTPException(status_code=404,detail="Not found")    

@router.get("/list/",response_model=list[TodoResponse])
async def get_todos(tags: Optional[str],
                    status: Optional[bool],
                    sort_by: str,
                    page: int,
                    page_size: int,
                    session: SessAsync):
    todos = await get_todos_from_db(Todo,tags,status,sort_by,page,page_size,session)
    return todos