# asgi.py

import uvicorn
from fastapi import FastAPI

from app.main import create_app
from app.config import settings

api: FastAPI = create_app(settings)

if __name__ == "__main__":
    uvicorn.run("asgi:api", host="0.0.0.0", port=8000, reload=True)
