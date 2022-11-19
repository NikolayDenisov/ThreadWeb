from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import persons as schema_person
from ..schemas import sensors as schema_sensor
from ..crud import persons as crud_persons
from ..utils import get_db

router = APIRouter()


@router.post("/persons/create", response_model=schema_person.PersonCreate)
def create_person(person: schema_person.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud_persons.get_person_by_email(db, email=person.email)
    if db_person:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_persons.create_person(db=db, person=person)


@router.get("/persons/", response_model=list[schema_person.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud_persons.get_persons(db, skip=skip, limit=limit)
    return persons


@router.get("/persons/{person_id}", response_model=schema_person.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud_persons.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@router.post("/persons/{person_id}/sensors/", response_model=schema_sensor.Sensor)
def create_sensor_for_person(person_id: int, sensor: schema_sensor.SensorCreate, db: Session = Depends(get_db)):
    return crud_persons.create_person_sensor(db=db, sensor=sensor, person_id=person_id)
