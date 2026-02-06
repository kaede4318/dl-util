from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging, os

from routes import router  # <-- import your router

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("app")

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    yield
    logger.info("Shutting down application")

# App
app = FastAPI(title="My Service", version="0.1.0", lifespan=lifespan)

# Mount routes under /api
app.include_router(router, prefix="/api")
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health & root
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Service is running"}

# Local entrypoint
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level=LOG_LEVEL.lower(),
        reload=True,
    )