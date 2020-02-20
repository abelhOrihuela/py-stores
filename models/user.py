from db import db
from requests import Response
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text
import uuid

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, default=str(uuid.uuid4()))
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_email_confirmation(self) -> Response:
        #call method to send emails
        print("Hola")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
