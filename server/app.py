"""CloudSense FastAPI application."""

import os

import uvicorn
from fastapi import FastAPI

from server.routes import router

app = FastAPI(title="CloudSense", version="1.0.0")
app.include_router(router)


def main() -> None:
    """Entry point for `server` console script and `python -m server.app`."""
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
