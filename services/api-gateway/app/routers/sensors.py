from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import sensors as crud_sensors
from ..schemas import sensors as schema_sensor
from ..utils import get_db

router = APIRouter()


@router.post("/sensors/create", response_model=schema_sensor.Sensor)
def create_sensor(sensor: schema_sensor.SensorCreate, db: Session = Depends(get_db)):
    db_sensor = crud_sensors.get_sensor_by_code(db, code=sensor.code)
    if db_sensor:
        raise HTTPException(status_code=400, detail="eui64 already registered")
    return crud_sensors.create_sensor(db=db, sensor=sensor)


@router.get("/sensors/", response_model=list[schema_sensor.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud_sensors.get_sensors(db, skip=skip, limit=limit)
    return sensors


@router.post("/sensors/value/", response_model=schema_sensor.Sensor)
def create_measured_value(measured_value: schema_sensor.MeasuredValueCreate, db: Session = Depends(get_db)):
    db_sensor = crud_sensors.get_sensor_by_code(db, code=measured_value.code)
    if not db_sensor:
        raise HTTPException(status_code=400, detail="eui64 unregistered")
    return crud_sensors.create_measured_value(db=db, measured_value=measured_value)


@router.post("/sensors/type/", response_model=schema_sensor.SensorTypeCreate)
def create_sensor_type(sensor_type: schema_sensor.SensorTypeCreate, db: Session = Depends(get_db)):
    return crud_sensors.create_sensor_type(db=db, sensor_type=sensor_type)


@router.post("/sensors/group/", response_model=schema_sensor.Sensor)
def create_sensor_group(sensor_group: schema_sensor.SensorGroupCreate, db: Session = Depends(get_db)):
    return crud_sensors.create_measured_value(db=db, sensor_group=sensor_group)


@router.post("/sensors/members/", response_model=schema_sensor.SensorGroupMembersCreate)
def create_sensor_group(sensor_members: schema_sensor.SensorGroupCreate, db: Session = Depends(get_db)):
    return crud_sensors.create_measured_value(db=db, sensor_members=sensor_members)


@router.post("/sensors/alert/", response_model=schema_sensor.SensorAlert)
def create_sensor_alert(sensor_alert: schema_sensor.SensorAlert, db: Session = Depends(get_db)):
    return crud_sensors.create_sensor_alert(db=db, sensor_alert=sensor_alert)


@router.get("/sensor/{sensor_code}", response_model=schema_sensor.Sensor)
def read_sensor(sensor_code: str, db: Session = Depends(get_db)):
    db_sensor = crud_sensors.get_sensor_by_code(db, sensor_code=sensor_code)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor
