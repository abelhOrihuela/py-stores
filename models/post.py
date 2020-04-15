from db import db
from libs.generate_uuid import generate_uuid
from typing import List
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import ARRAY, array


class PostModel(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), nullable=False, unique=True, default=generate_uuid)
    title = db.Column(db.String(500), nullable=False)
    subtitle = db.Column(db.String(500), nullable=False)
    tags = db.Column(
        ARRAY(db.Text),
        nullable=False,
        default=db.cast(array([], type_=db.Text), ARRAY(db.Text)),
    )
    content = db.Column(JSONB)
    author = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    @classmethod
    def find_all(cls) -> List["PostModel"]:
        return cls.query.all()

    @classmethod
    def find_by_uuid(cls, _uuid: str) -> "PostModel":
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
