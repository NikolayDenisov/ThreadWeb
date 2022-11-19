from datetime import datetime

from sqlalchemy.orm import Session

from ..models import sensors as models_sensors
from ..schemas import sensors as schema_sensor


def create_sensor(db: Session, sensor: schema_sensor.SensorCreate):
    db_sensor = models_sensors.Sensor(id_type=sensor.id_type, id_owner=sensor.id_owner, code=sensor.code,
                                      name=sensor.name, description=sensor.description,
                                      date_created=datetime.now())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_sensor_by_code(db: Session, code: str):
    return db.query(models_sensors.Sensor).filter(models_sensors.Sensor.code == code).first()


def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_sensors.Sensor).offset(skip).limit(limit).all()


def create_sensor_type(db: Session, sensor_type: schema_sensor.SensorTypeCreate):
    db_sensor_type = models_sensors.SensorType(name=sensor_type.name, unit=sensor_type.unit,
                                               description=sensor_type.description)
    db.add(db_sensor_type)
    db.commit()
    db.refresh(db_sensor_type)
    return db_sensor_type


def create_sensor_group(db: Session, sensor_group: schema_sensor.SensorGroupCreate):
    db_sensor_group = models_sensors.SensorGroup(id_type=sensor_group.id_type, code=sensor_group.code,
                                                 name=sensor_group.name)
    db.add(db_sensor_group)
    db.commit()
    db.refresh(db_sensor_group)
    return db_sensor_group


def create_measured_value(db: Session, measured_value: schema_sensor.MeasuredValueCreate):
    db_measured_value = models_sensors.MeasuredValue(id_sensor=measured_value.id_sensor, date_measured=datetime.now(),
                                                     value=measured_value.value)
    db.add(db_measured_value)
    db.commit()
    db.refresh(db_measured_value)
    return db_measured_value


def create_sensor_group_members(db: Session, sensor_group_members: schema_sensor.SensorGroupMembersCreate):
    db_sensor_group_members = models_sensors.SensorGroupMembers(group_id=sensor_group_members.group_id,
                                                                sensor_id=sensor_group_members.sensor_id)
    db.add(db_sensor_group_members)
    db.commit()
    db.refresh(db_sensor_group_members)
    return db_sensor_group_members


def create_sensor_alert(db: Session, sensor_alert: schema_sensor.SensorAlert):
    db_sensor_alert = models_sensors.Alert(id_sensor=sensor_alert.id_sensor,
                                           threshold=sensor_alert.threshold,
                                           alert_mode=sensor_alert.alert_mode,
                                           mail_recipient=sensor_alert.mail_recipient,
                                           mail_subject=sensor_alert.mail_subject)
    db.add(db_sensor_alert)
    db.commit()
    db.refresh(db_sensor_alert)
    return db_sensor_alert


def get_values(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_sensors.MeasuredValue).offset(skip).limit(limit).all()
