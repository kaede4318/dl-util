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

@router.post("/submit")
async def submit_link(data: LinkData):
    # do something with data.link
    return {"received": data.link, "message": "Link submitted successfully"}

