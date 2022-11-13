from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/persons/", response_model=schemas.Person)
def create_user(user: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, person=user)


@app.get("/persons/", response_model=list[schemas.Person])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_persons(db, skip=skip, limit=limit)
    return users


@app.get("/persons/{user_id}", response_model=schemas.Person)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_person(db, person_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_user


@app.post("/persons/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_sensors(db, skip=skip, limit=limit)
    return items
