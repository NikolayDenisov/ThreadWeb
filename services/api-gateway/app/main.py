from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/persons/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.get_person_by_email(db, email=person.email)
    if db_person:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_person(db=db, person=person)


@app.get("/persons/", response_model=list[schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit)
    return persons


@app.get("/persons/{person_id}", response_model=schemas.Person)
def read_peson(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@app.post("/persons/{person_id}/sensors/", response_model=schemas.Sensor)
def create_sensor_for_person(
        person_id: int, sensor: schemas.SensorCreate, db: Session = Depends(get_db)
):
    return crud.create_person_sensor(db=db, sensor=sensor, person_id=person_id)


@app.get("/sensors/", response_model=list[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud.get_sensors(db, skip=skip, limit=limit)
    return sensors
