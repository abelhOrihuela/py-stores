from typing import List
from requests import Response

from flask import render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os


class Mailer:
    @classmethod
    def send_email(
        cls, email: List[str], subject: str, template: str, data
    ) -> Response:

        message = Mail(
            from_email="hola@blazepixel.mx",
            to_emails=email,
            subject=subject,
            html_content=render_template(template + ".html", data=data),
        )

        try:
            sg = SendGridAPIClient(os.getenv("SENDGRID_KEY"))
            sg.send(message)
            return {"message": "Email has been sent"}, 200

        except Exception as e:
            print(str(e))

            return {"message": "An error ocurred when processing your request"}, 500
