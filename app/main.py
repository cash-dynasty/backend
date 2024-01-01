from fastapi import FastAPI

# import models
from database import engine
from routers import auth

# models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
print('Base')
app.include_router(auth.app)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
