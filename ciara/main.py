import logging

from fastapi import FastAPI
from starlette import status

from router import orchestrator
from models.database import Base, engine


logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine, checkfirst=True)


app = FastAPI(title="Ciara App",
              description="Test Orchastration Application.",
              version="0.0.1")

app.include_router(orchestrator.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def home() -> dict[str, str]:
    return {"message": "Welcome to Ciara!"}
