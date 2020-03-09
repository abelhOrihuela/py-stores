from flask_restful import Resource
from models.state import StateModel
from schemas.state import StateSchema
from flask import request

state_schema = StateSchema()
state_schema_list = StateSchema(many=True)


class State(Resource):
    @classmethod
    def get(cls, uuid: str):
        state = StateModel.find_by_uuid(uuid)

        if not state:
            return {"message": "State not found"}, 404

        return state_schema.dump(state), 200

    @classmethod
    def put(cls, uuid: str):
        state = StateModel.find_by_uuid(uuid)
        state_json = request.get_json()
        state_schema.load(state_json)

        if not state:
            return {"message": "State not found"}, 404

        state.name = state_json["name"]
        state.abbr = state_json["abbr"]

        state.save_to_db()

        return {"Message": "State updated succesfully"}, 200

    @classmethod
    def delete(cls, uuid: str):
        state = StateModel.find_by_uuid(uuid)

        if not state:
            return {"message": "State not found"}, 404

        state.delete_from_db()

        return {"message": "State deleted"}, 200


class States(Resource):
    @classmethod
    def get(cls):

        return {"states": state_schema_list.dump(StateModel.find_all())}

    @classmethod
    def post(cls):
        state_request = state_schema.load(request.get_json())
        state_request.save_to_db()
        return {"message": "State created succesfully"}, 201
