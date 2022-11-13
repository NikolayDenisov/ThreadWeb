from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class SensorBase(BaseModel):
    description: str | None = None


class SensorCreate(SensorBase):
    pass


class Sensor(SensorBase):
    id: int
    id_owner: int

    class Config:
        orm_mode = True


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
