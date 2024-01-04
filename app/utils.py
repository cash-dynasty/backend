import resend
from passlib.context import CryptContext

resend.api_key = "re_gKSV3gL4_HERpk4eofjnbJ6Z36wH5dTyf"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def send_user_create_email_confirmation(email: str, token: str):
    with open("templates/testemail.html", "r") as file:
        html = file.read()
        html = html.replace("{{{TOKEN}}}", token)
    params = {
        "from": "Developer CashDynasty <no-replay@cashdynasty.pl>",
        "to": [email],
        "subject": "Chyba działa :D",
        "html": html,
    }
    email = resend.Emails.send(params)
    return email


# print(send_user_create_email_confirmation('dev@cashdynasty.pl', 'tokenik'))

