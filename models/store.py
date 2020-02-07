from typing import Dict, List, Union
from db import db
from serializers.item import ItemJSON
from serializers.store import StoreJSON

class StoreModel(db.Model):
    # table of SQL
    __tablename__ = "stores"

    # Strucuture of table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self) -> StoreJSON:
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
