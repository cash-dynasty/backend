from pydantic import BaseModel, ConfigDict
from schemas.user import UserBase


class PlayerSetNicknameReq(BaseModel):
    player_name: str


class PlayerSetNicknameRes(UserBase):
    pass

    model_config = ConfigDict(from_attributes=True)
