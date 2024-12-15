from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/todo",
    tags = ["todo"]
)
