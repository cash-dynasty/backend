from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routers import auth, test, users


app = FastAPI(redoc_url=None)

app.include_router(auth.router)
app.include_router(test.router)
app.include_router(users.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CashDynasty FastAPI Docs",
        version="0.1.0",
        openapi_version="3.0.3",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
