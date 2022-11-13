from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import sensors as crud_sensors
from ..schemas import schemas
from ..utils import get_db

router = APIRouter()


@router.post("/sensors/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    db_sensor = crud_sensors.get_sensor_by_code(db, code=sensor.code)
    if db_sensor:
        raise HTTPException(status_code=400, detail="eui64 already registered")
    return crud_sensors.create_sensor(db=db, sensor=sensor)


@router.get("/sensors/", response_model=list[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud_sensors.get_sensors(db, skip=skip, limit=limit)
    return sensors


@router.post("/sensors/value/", response_model=schemas.Person)
def create_measured_value(measured_value: schemas.MeasuredValueCreate, db: Session = Depends(get_db)):
    db_sensor = crud_sensors.get_sensor_by_code(db, code=measured_value.code)
    if not db_sensor:
        raise HTTPException(status_code=400, detail="eui64 unregistered")
    return crud_sensors.create_measured_value(db=db, measured_value=measured_value)
