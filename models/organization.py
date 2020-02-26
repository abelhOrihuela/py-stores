from db import db
from typing import List
from models.users_organizations import users_organizations
from models.project import ProjectModel
from generate_uuid import generate_uuid


class OrganizationModel(db.Model):

    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, unique=True, default=generate_uuid)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship(
        "UserModel", secondary=users_organizations, back_populates="organizations"
    )

    projects = db.relationship("ProjectModel", lazy="dynamic")

    @classmethod
    def find_by_name(cls, _name: str) -> "OrganizationModel":
        return cls.query.filter_by(name=_name).first()

    @classmethod
    def find_all(cls) -> List["OrganizationModel"]:
        return cls.query.all()

    @classmethod
    def find_by_uuid(cls, _uuid: str) -> "OrganizationModel":
        return cls.query.filter_by(uuid=_uuid).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
