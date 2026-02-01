from fastapi import FastAPI

from app.core.database import Base, engine
from app.models import user
from app.api.v1 import auth

app = FastAPI(title="Support Ticket Management API")

app.include_router(auth.router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


