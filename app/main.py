from exceptions import CustomHTTPException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import auth, test, users


app = FastAPI()

app.include_router(auth.router)
app.include_router(test.router)
app.include_router(users.router)


@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
        headers=exc.headers,
    )
