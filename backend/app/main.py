from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings

app = FastAPI(title=get_settings().app_name, version="0.1.0")


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}


app.include_router(router)
