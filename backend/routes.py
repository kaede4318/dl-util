# routes.py
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from downloader import run

router = APIRouter()

class LinkData(BaseModel):
    link: str

@router.get("/hello")
async def say_hello():
    return {"message": "Hello from /api/hello!"}

@router.post("/download")
async def download_link(data: LinkData):
    print(f"Download request for link: {data.link}")  # log every request
    fp = run(data.link) # download video
    print("name",fp.name)

    return FileResponse(
        path=str(fp), 
        filename=fp.name,
        media_type="video/mp4",
        headers={"Cache-Control": "no-store"}
    )

