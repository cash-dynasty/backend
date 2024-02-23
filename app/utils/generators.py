import secrets
from datetime import timedelta

from settings import settings
from utils.commons import get_current_time


def generate_activation_token():
    token = "".join(secrets.token_hex(32))
    expiration_date = (get_current_time() + timedelta(minutes=settings.ACTIVATION_TOKEN_EXPIRE_MINUTES)).isoformat()
    return {"token": token, "expiration_date": expiration_date}
