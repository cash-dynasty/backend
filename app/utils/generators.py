import secrets
from datetime import datetime, timedelta

from settings import settings


def generate_activation_token():
    token = "".join(secrets.token_hex(32))
    expiration_date = (datetime.utcnow() + timedelta(minutes=settings.ACTIVATION_TOKEN_EXPIRE_MINUTES)).isoformat()
    return {"token": token, "expiration_date": expiration_date}
