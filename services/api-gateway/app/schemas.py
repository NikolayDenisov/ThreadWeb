from pydantic import BaseModel


class SensorBase(BaseModel):
    description: str | None = None


class ItemCreate(SensorBase):
    pass


class Item(SensorBase):
    id: int
    id_owner: int

    class Config:
        orm_mode = True


class PersonBase(BaseModel):
    email: str


class PersonCreate(PersonBase):
    password: str


class Person(PersonBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
