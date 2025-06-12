import yagmail
import os

class Email():
    def __init__(self):
        password = os.environ.get("ZOHO_PASSWORD")
        if not password:
            raise ValueError("Environment variable 'ZOHO_PASSWORD' not set!")
        self.mail_service = yagmail.SMTP(user="log@dtdevltd.com", password=password, host="smtp.zoho.eu", port=465)

    def send(self, subject, contents):
        self.mail_service.send(to="declantugwell@dtdevltd.com", subject=subject, contents=contents)