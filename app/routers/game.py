import re

import schemas.game.start
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import User
from sqlalchemy.orm import Session
from utils.auth import get_current_active_user, get_current_user

from app.models.user import User as MUser


router = APIRouter(
    prefix="/game",
    tags=["game"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post(
    "/start/nickname",
    status_code=status.HTTP_200_OK,
    response_model=schemas.game.start.SetPlayerNameOut,
)
async def game_start_set_nickname(
    updated_user: schemas.game.start.SetPlayerNameIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_query = db.query(MUser).filter(MUser.id == current_user.id)
    updated_user.player_name = updated_user.player_name.strip()
    pattern = re.compile("^[a-zA-Z0-9]{3,}$")
    is_player_name_match = pattern.match(updated_user.player_name)
    if not is_player_name_match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid player name")

    print(user_query)
    user_query.update(updated_user.model_dump())
    # new_user = models.user.User(**user.model_dump())
    # db.add(new_user)
    db.commit()
    return user_query
