from fastapi import FastAPI, HTTPException
from routes import hello

app = FastAPI()
app.include_router(hello.router, prefix='/hello', tags=['hello'])