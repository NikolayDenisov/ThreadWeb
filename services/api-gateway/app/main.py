from fastapi import FastAPI

from .models.database import engine, Base
from .routers import persons, sensors

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(sensors.router)
