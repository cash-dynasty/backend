from pydantic import BaseModel


class StatusMessageRes(BaseModel):
    status_code: int
    message: str
    headers: dict | None = None
