import resend

from settings import RESEND_API_KEY

resend.api_key = RESEND_API_KEY


def send_user_create_confirmation_email(email: str, token: str):
    with open("../templates/testemail.html", "r") as file:
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
