from db import db
from typing import List
from models.users_organizations import users_organizations
import uuid

class OrganizationModel(db.Model):

    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, default=str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True)
    users = db.relationship(
        "UserModel",
        secondary=users_organizations,
        back_populates="organizations"
    )

    @classmethod
    def find_by_uuid(cls, _uuid: str) -> "Organization":
        return cls.query.filter_by(uuid=_uuid).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()