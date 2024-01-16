import pytest
import schemas.game.start
import schemas.user
from fastapi import status
from routers.game import game_start_set_nickname


# dictionary with id key and value of 2
mockedUser = schemas.user.User(
    email="test@test.com", id=2, is_active=True, player_name="testplayername", password="test"
)


@pytest.mark.asyncio
async def test_game_start_set_nickname(dbsession, monkeypatch):
    # Przygotowanie danych testowych
    test_user_id = 1
    test_user_nickname = "testname"
    test_request_data = schemas.game.start.PlayerSetNicknameReq(
        player_name=test_user_nickname, current_user={"id": test_user_id}
    )

    # Mockowanie funkcji zależności (np. get_db i get_current_user)
    monkeypatch.setattr("database.get_db", lambda: dbsession)  # Mockowanie get_db

    async def mock_get_current_user():
        return schemas.user.User(id=test_user_id)

    monkeypatch.setattr("utils.auth.get_current_user", mock_get_current_user)  # Mockowanie get_current_user

    # Wywołanie funkcji
    response = await game_start_set_nickname(test_request_data)

    # Sprawdzenie, czy odpowiedź ma poprawny kod statusu
    assert response.status_code == status.HTTP_200_OK

    # Sprawdzenie, czy odpowiedź ma oczekiwane dane
    assert response.json()["player_name"] == test_user_nickname


# @pytest.mark.asyncio
# async def test_game_start_set_nickname_success(dbsession):
#     updated_user = schemas.game.start.PlayerSetNicknameReq(player_name="testplayername")
#     set_nickname = await game_start_set_nickname(updated_user=updated_user, db=dbsession, current_user=mockedUser)
#     assert set_nickname.player_name == updated_user.player_name


# @pytest.mark.asyncio
# async def test_game_start_set_nickname_forbidden_characters(dbsession):
#     with pytest.raises(pydantic_core._pydantic_core.ValidationError) as PlayerNameValidation:
#         test_user = schemas.game.start.PlayerSetNicknameReq(player_name="pl@yer")
#         await game_start_set_nickname(updated_user=test_user, db=dbsession, current_user=mockedUser)
#     assert "string does not match regex" in PlayerNameValidation.value.errors()[0]["msg"]
#
#
# @pytest.mark.asyncio
# async def test_game_start_set_nickname_too_short(dbsession):
#     with pytest.raises(pydantic_core._pydantic_core.ValidationError) as PlayerNameValidation:
#         test_user = schemas.game.start.PlayerSetNicknameReq(player_name="te")
#         await game_start_set_nickname(updated_user=test_user, db=dbsession, current_user=mockedUser)
#     assert "string does not match regex" in PlayerNameValidation.value.errors()[0]["msg"]
