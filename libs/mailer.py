from typing import List
from requests import Response

class Mailer:

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html:str) -> Response:
        