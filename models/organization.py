from db import db
from typing import List
from models.users_organizations import users_organizations
from libs.generate_uuid import generate_uuid


class OrganizationModel(db.Model):

    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, unique=True, default=generate_uuid)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship(
        "UserModel", secondary=users_organizations, back_populates="organizations"
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    @classmethod
    def find_by_name(cls, _name: str) -> "OrganizationModel":
        return cls.query.filter_by(name=_name).first()

    @classmethod
    def find_all(cls) -> List["OrganizationModel"]:
        return cls.query.all()

    @classmethod
    def find_by_uuid(cls, _uuid: str) -> "OrganizationModel":
        return cls.query.filter_by(uuid=_uuid).first()

    @classmethod
    def count(cls) -> int:
        return cls.query.count()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
