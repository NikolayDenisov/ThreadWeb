from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/sensor/list")
def get_sensor_list():
    return {"item_id": 0, "q": 0}


@app.get("/sensor/{sensor_id}")
def read_sensor_value(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
