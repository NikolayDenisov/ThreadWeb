from sqlalchemy import (Boolean, Column,
                        ForeignKey, Integer,
                        String, TIMESTAMP,
                        Float)
from sqlalchemy import event, DDL

from .database import Base


class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True, index=True)
    id_type = Column(Integer, ForeignKey("sensor_type.id"))
    id_owner = Column(Integer, ForeignKey("person.id"))
    code = Column(String(20))
    name = Column(String(50))
    description = Column(String(80))
    date_created = Column(TIMESTAMP(timezone=True))


class SensorType(Base):
    __tablename__ = 'sensor_type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    unit = Column(String(14))
    description = Column(String(160))


class SensorGroup(Base):
    __tablename__ = 'sensor_group'
    id = Column(Integer, primary_key=True, index=True)
    id_type = Column(Integer, ForeignKey("sensor_type.id"))
    code = Column(String(20))
    name = Column(String(50))


class SensorGroupMembers(Base):
    __tablename__ = 'sensor_group_members'
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("sensor_group.id"))
    sensor_id = Column(Integer, ForeignKey("sensor.id"))


class MeasuredValue(Base):
    __tablename__ = 'measured_value'
    id = Column(Integer, primary_key=True, index=True)
    id_sensor = Column(Integer, ForeignKey("sensor.id"))
    date_measured = Column(TIMESTAMP(timezone=True))
    value = Column(Float(precision=2))


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    description = Column(String(160))
    is_active = Column(Boolean, default=True)


class Alert(Base):
    __tablename__ = 'alert'
    id = Column(Integer, primary_key=True, index=True)
    id_sensor = Column(Integer, ForeignKey("sensor.id"))
    threshold = Column(Float(precision=2))
    active = Column(Boolean, nullable=False)
    alert_mode = Column(String(8))
    mail_recipient = Column(String(30))
    mail_subject = Column(String(50))


@event.listens_for(MeasuredValue.__table__, "after_create")
def receive_after_create(connection):
    DDL(
        f"SELECT create_hypertable('measured_value','date_measured');"
    ).execute(connection)
