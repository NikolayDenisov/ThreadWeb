from datetime import datetime

from sqlalchemy.orm import Session

from ..models import sensors as models_sensors
from ..schemas import schemas


def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models_sensors.Sensor(id_type=sensor.id_type, id_owner=sensor.id_owner, code=sensor.code,
                                      name=sensor.name, description=sensor.description,
                                      date_created=datetime.now())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_sensor_by_code(db: Session, code: str):
    return db.query(models_sensors.Person).filter(models_sensors.Sensor.code == code).first()


def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_sensors.Sensor).offset(skip).limit(limit).all()


def create_sensor_type(db: Session, sensor_type: schemas.SensorTypeCreate):
    db_sensor_type = models_sensors.SensorType(name=sensor_type.name, unit=sensor_type.unit,
                                               description=sensor_type.description)
    db.add(db_sensor_type)
    db.commit()
    db.refresh(db_sensor_type)
    return db_sensor_type


def create_sensor_group(db: Session, sensor_group: schemas.SensorGroupCreate):
    db_sensor_group = models_sensors.SensorGroup(id_type=sensor_group.id_type, code=sensor_group.code,
                                                 name=sensor_group.name)
    db.add(db_sensor_group)
    db.commit()
    db.refresh(db_sensor_group)
    return db_sensor_group


def create_measured_value(db: Session, measured_value: schemas.MeasuredValueCreate):
    db_measured_value = models_sensors.MeasuredValue(id_sensor=measured_value.id_sensor, date_measured=datetime.now(),
                                                     value=measured_value.value)
    db.add(db_measured_value)
    db.commit()
    db.refresh(db_measured_value)
    return db_measured_value
