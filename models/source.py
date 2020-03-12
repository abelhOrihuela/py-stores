from db import db
from lib.generate_uuid import generate_uuid
from typing import List


class SourceModel(db.Model):
    __tablename__ = "sources"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, unique=True, default=generate_uuid)
    name = db.Column(db.String(80), nullable=False)
    site = db.Column(db.String(500), nullable=False)
    title_selector = db.Column(db.String(500), nullable=False)
    subtitle_selector = db.Column(db.String(500))
    tags_selector = db.Column(db.String(500))
    content_selector = db.Column(db.String(500), nullable=False)
    author_selector = db.Column(db.String(500))

    @classmethod
    def find_all(cls) -> List["SourceModel"]:
        return cls.query.all()

    @classmethod
    def find_by_uuid(cls, _uuid: str) -> "SourceModel":
        return cls.query.filter_by(uuid=_uuid).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
