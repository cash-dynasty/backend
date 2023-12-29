from fastapi import FastAPI, Depends

from .routers import auth

app = FastAPI()

app.include_router(auth.app)


@app.get("/")
def read_root():
    return {"Hello": "World"}
