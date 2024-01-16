from typing import Annotated

import schemas.user
from fastapi import Depends, FastAPI
from routers import auth, game, test, users
from utils.auth import get_current_active_user


app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(game.router)
app.include_router(test.router)
app.include_router(test.router_public)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/protected")
def read_protected_endpoint(current_user: Annotated[schemas.user.UserBase, Depends(get_current_active_user)]):
    return {"message": "This is a protected endpoint."}
