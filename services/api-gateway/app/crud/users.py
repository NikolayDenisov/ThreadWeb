from sqlalchemy.orm import Session

from ..models import users as models_users
from ..schemas import users as schema_user
from ..schemas import sensors as schema_sensor


def get_user(db: Session, user_id: int):
    return db.query(models_users.User).filter(models_users.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models_users.User).filter(models_users.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_users.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema_user.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models_users.User(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_sensor(db: Session, sensor: schema_sensor.SensorCreate, user_id: int):
    db_sensor = models_users.Sensor(**sensor.dict(), id_owner=user_id)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor
