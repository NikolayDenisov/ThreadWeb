from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class SensorBase(BaseModel):
    name: str | None = None
    description: str


class SensorCreate(SensorBase):
    id_type: int
    id_owner: int
    code: str


class SensorTypeCreate(SensorBase):
    unit: str


class SensorGroupCreate(SensorBase):
    unit: str


class Sensor(SensorBase):
    id: int
    id_type: int
    id_owner: int
    code: str
    date_created: datetime

    class Config:
        orm_mode = True


class MeasuredValueBase(BaseModel):
    id: int
    id_sensor: int
    date_measured: datetime
    value: float

    class Config:
        orm_mode = True


class MeasuredValueCreate(BaseModel):
    id_sensor: int
    date_measured: datetime
    value: float
    code: str


class SensorGroupCreate(MeasuredValueBase):
    unit: str


class PersonBase(BaseModel):
    email: EmailStr


class PersonCreate(PersonBase):
    password: str


class Person(PersonBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        """ Конвертирует UUID в hex строку """
        return value.hex
