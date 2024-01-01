from fastapi import FastAPI

from routers import auth, users

# import models

# models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()

app.include_router(auth.app)
app.include_router(users.app)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
