from flask_restful import Resource
from models.store import StoreModel
from schemas.store import StoreSchema

from utils.messages import ERROR_BLANK_FIELD, NOT_FOUND, ERROR_INSERTING

store_schema = StoreSchema()
stores_list_schema = StoreSchema(many=True)

class Store(Resource):

    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {"message": NOT_FOUND.format("Store")}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return (
                {"message": "A store with name '{}' already exists.".format(name)},
                400,
            )

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format("Stote")}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted."}


class StoreList(Resource):

    @classmethod
    def get(cls):
        return {"stores": stores_list_schema.dump(StoreModel.find_all())}
