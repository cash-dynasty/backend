from typing import Annotated

from fastapi import FastAPI, Depends

from dependencies import get_current_active_user
from routers import auth, users
from schemas import User

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/protected")
def read_protected_endpoint(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {"message": "This is a protected endpoint."}
