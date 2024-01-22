import secrets
from datetime import datetime, timedelta


def generate_activation_token():
    token = "".join(secrets.token_hex(32))
    expiration_date = (datetime.utcnow() + timedelta(hours=1)).isoformat()
    return {"token": token, "expiration_date": expiration_date}
