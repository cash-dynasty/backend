import resend
from settings import settings


resend.api_key = settings.RESEND_API_KEY


def send_user_create_confirmation_email(email: str, token: str):
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
