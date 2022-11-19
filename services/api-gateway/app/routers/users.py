from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import users as schema_user
from ..schemas import sensors as schema_sensor
from ..crud import users as crud_users
from ..utils import get_db

router = APIRouter()


@router.post("/users/create", response_model=schema_user.UserCreate)
def create_user(user: schema_user.User, db: Session = Depends(get_db)):
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_users.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schema_user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_users.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schema_user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/sensors/", response_model=schema_sensor.Sensor)
def create_sensor_for_user(user_id: int, sensor: schema_sensor.SensorCreate, db: Session = Depends(get_db)):
    return crud_users.create_user_sensor(db=db, sensor=sensor, user_id=user_id)
