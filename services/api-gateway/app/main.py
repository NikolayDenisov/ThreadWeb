from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.database import engine, Base
from .routers import persons, sensors

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://panel.sinbiot.ru",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(persons.router)
app.include_router(sensors.router)
