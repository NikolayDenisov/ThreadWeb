from sqlalchemy.orm import Session

from ..models import persons as models_persons
from ..schemas import persons as schema_person
from ..schemas import sensors as schema_sensor


def get_person(db: Session, person_id: int):
    return db.query(models_persons.Person).filter(
        models_persons.Person.id == person_id).first()


def get_person_by_email(db: Session, email: str):
    return db.query(models_persons.Person).filter(
        models_persons.Person.email == email).first()


def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_persons.Person).offset(skip).limit(limit).all()


def create_person(db: Session, person: schema_person.PersonCreate):
    fake_hashed_password = person.password + "notreallyhashed"
    db_person = models_persons.Person(first_name=person.first_name,
                                      last_name=person.last_name,
                                      email=person.email,
                                      password=fake_hashed_password)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def create_person_sensor(db: Session, sensor: schema_sensor.SensorCreate,
                         person_id: int):
    db_sensor = models_persons.Sensor(**sensor.dict(), id_owner=person_id)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor
