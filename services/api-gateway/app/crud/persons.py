from sqlalchemy.orm import Session

from ..models import persons as models_persons
from ..schemas import schemas


def get_person(db: Session, person_id: int):
    return db.query(models_persons.Person).filter(models_persons.Person.id == person_id).first()


def get_person_by_email(db: Session, email: str):
    return db.query(models_persons.Person).filter(models_persons.Person.email == email).first()


def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_persons.Person).offset(skip).limit(limit).all()


def create_person(db: Session, person: schemas.PersonCreate):
    fake_hashed_password = person.password + "notreallyhashed"
    db_person = models_persons.Person(email=person.email, hashed_password=fake_hashed_password)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def create_person_sensor(db: Session, sensor: schemas.SensorCreate, person_id: int):
    db_sensor = models_persons.Sensor(**sensor.dict(), id_owner=person_id)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor
