from pydantic import BaseModel
from schemas.user import User


class SetPlayerNameIn(BaseModel):
    player_name: str


class SetPlayerNameOut(BaseModel):
    updated_user: User
