from datetime import datetime

from pydantic import BaseModel


class SensorBase(BaseModel):
    name: str | None = None
    description: str

    class Config:
        orm_mode = True


class SensorCreate(SensorBase):
    id_type: int
    id_owner: int
    code: str


class SensorTypeCreate(SensorBase):
    unit: str


class SensorGroupCreate(SensorBase):
    id_type: int
    code: str


class SensorGroupMembersCreate(BaseModel):
    group_id: int
    sensor_id: int


class Sensor(SensorBase):
    id_type: int
    id_owner: int
    code: str
    date_created: datetime

    class Config:
        orm_mode = True


class MeasuredValueBase(BaseModel):
    id_sensor: int
    date_measured: datetime
    value: float

    class Config:
        orm_mode = True


class MeasuredValueCreate(BaseModel):
    id_sensor: int
    date_measured: datetime
    value: float

    class Config:
        orm_mode = True


class SensorAlert(BaseModel):
    id_sensor: int
    threshold: float
    active: bool
    alert_mode: str
    mail_recipient: str
    mail_subject: str
