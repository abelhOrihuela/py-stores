from db import db
from generate_uuid import generate_uuid
from typing import List

class MunicipalityModel(db.Model):

    __tablename__ = "municipalities"


    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, unique=True, default=generate_uuid)
    name = db.Column(db.String(80), nullable=False)
    abbr = db.Column(db.String(80), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"))
    store = db.relationship("StateModel")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    @classmethod
    def find_all(cls) -> List["MunicipalityModel"]:
        cls.query.all()

    @classmethod
    def find_by_uuid(cls, _uuid: str) -> "MunicipalityModel":
        return cls.query.filter_by(uuid=_uuid).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


