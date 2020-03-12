from db import db
from requests import Response
from models.organization import OrganizationModel
from models.users_organizations import users_organizations
from lib.generate_uuid import generate_uuid


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, unique=True, default=generate_uuid)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    activated = db.Column(db.Boolean, default=False)
    organizations = db.relationship(
        "OrganizationModel", secondary=users_organizations, back_populates="users"
    )

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_uuid(cls, _uuid: str) -> "UserModel":
        return cls.query.filter_by(uuid=_uuid).first()

    def send_email_confirmation(self) -> Response:
        # call method to send emails
        print("Hola")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
