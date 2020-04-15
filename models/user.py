from db import db
from requests import Response
from models.organization import OrganizationModel
from models.users_organizations import users_organizations
from libs.generate_uuid import generate_uuid
from typing import List
from libs.mailer import Mailer
import os


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, unique=True, default=generate_uuid)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    activated = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), default="user")
    organizations = db.relationship(
        "OrganizationModel", secondary=users_organizations, back_populates="users"
    )

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_uuid(cls, _uuid: str) -> "UserModel":
        return cls.query.filter_by(uuid=_uuid).first()

    @classmethod
    def count(cls) -> int:
        return cls.query.count()

    def send_email_confirmation(self) -> Response:
        mailer = Mailer()

        return mailer.send_email(
            "abel@commonsense.io",
            "Confirmación registro",
            "user-confirm",
            {
                "to": "abel@commonsense.io",
                "message": "Hola",
                "username": self.username,
                "url": os.getenv("APP_HOST") + "/user-confirm/" + self.uuid,
            },
        )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
