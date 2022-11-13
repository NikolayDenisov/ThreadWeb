from sqlalchemy.orm import Session

from ..models import sensors as models_sensors


def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_sensors.Sensor).offset(skip).limit(limit).all()
