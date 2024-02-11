from pydantic import BaseModel


class MessageRes(BaseModel):
    detail: str
