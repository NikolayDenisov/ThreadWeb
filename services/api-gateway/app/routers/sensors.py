from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud import sensors as crud_sensors
from ..schemas import schemas
from ..utils import get_db

router = APIRouter()


@router.get("/sensors/", response_model=list[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sensors = crud_sensors.get_sensors(db, skip=skip, limit=limit)
    return sensors
