from typing import Annotated

import schemas.user
from fastapi import Depends, FastAPI
from routers import auth, users
from utils.auth import get_current_active_user


app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def read_root_endpoint():
    return {"message": "Hello from public endpoint!"}


@app.get("/protected")
def read_protected_endpoint(current_user: Annotated[schemas.user.User, Depends(get_current_active_user)]):
    return {"message": "Hello from protected endpoint!"}
