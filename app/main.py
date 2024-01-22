from fastapi import FastAPI
from routers import auth, test, users


app = FastAPI()

app.include_router(auth.router)
app.include_router(test.router)
app.include_router(users.router)
