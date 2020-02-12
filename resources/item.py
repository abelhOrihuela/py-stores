from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
)
from marshmallow import ValidationError
from models.item import ItemModel
from schemas.item import ItemSchema
from utils.messages import ERROR_BLANK_FIELD, NOT_FOUND, ERROR_INSERTING

item_schema = ItemSchema()
items_list_schema = ItemSchema(many=True)

class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {"message": NOT_FOUND.format("Item")}, 404

    @classmethod
    @jwt_required
    def post(cls, name: str):

        item_json = request.get_json()
        item_json["name"] = name

        try:
            item = item_schema.load(item_json)
        except ValidationError as error:
            return error.messages, 400

        if ItemModel.find_by_name(name):
            return (
                {"message": "An item with name '{}' already exists.".format(name)},
                400,
            )

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format("Item")}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}, 200
        return {"message": NOT_FOUND.format("Item")}, 404

    @classmethod
    @jwt_required
    def put(cls, name: str):
        item_json = request.get_json()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name
            try:
                item = item_schema.load(item_json)
            except ValidationError as error:
                return error.messages, 400

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemList(Resource):

    @classmethod
    def get(cls):
        return { "items": items_list_schema.dump(ItemModel.find_all()) }, 200
