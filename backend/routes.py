# routes.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from downloader import run

router = APIRouter()

class LinkData(BaseModel):
    link: str

@router.get("/hello")
async def say_hello():
    return {"message": "Hello from /api/hello!"}

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id, "description": f"Item {item_id} details"}

@router.post("/submit")
async def submit_link(data: LinkData):
    # do something with data.link
    return {"received": data.link, "message": "Link submitted successfully"}

