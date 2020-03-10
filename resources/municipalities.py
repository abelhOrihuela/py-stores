from flask_restful import Resource
from flask import request
from models.municipality import MunicipalityModel
from models.state import StateModel
from schemas.municipality import MunicipalitySchema
from flask_jwt_extended import (
    jwt_required
)
municipality_schema = MunicipalitySchema()
municipality_schema_list = MunicipalitySchema(many=True)

class Municipality(Resource):
    @classmethod
    def get(cls, uuid: str):
        municipality = MunicipalityModel.find_by_uuid(uuid)
        if not municipality:
            return {
                "message": "Municipality not found"
            }, 404

        return municipality_schema.dump(municipality)
    
    @classmethod
    @jwt_required
    def put(cls, uuid: str):
        municipality_json = request.get_json()
        municipality_schema.load(municipality_json)
        municipality = MunicipalityModel.find_by_uuid(uuid)

        if not municipality:
            return {
                "message": "Municipality not found"
            }, 404

        municipality.name = municipality_json["name"]
        municipality.abbr = municipality_json["abbr"]
        municipality.state_id = municipality_json["state_id"]
        municipality.save_to_db()

        return {"Message": "Municipality updated successfully"}, 200

    
    @classmethod
    @jwt_required
    def delete(cls, uuid: str):
        municipality = MunicipalityModel.find_by_uuid(uuid)
        if not municipality:
            return {
                "message": "Municipality not found"
            }, 404
        return {
            "message": "Municipality deleted"
        }, 200
    

class Municipalities(Resource):
    @classmethod
    def get(cls):

        return {
            "municipalities": municipality_schema_list.dump(MunicipalityModel.find_all())
        }, 200

    @classmethod
    @jwt_required
    def post(cls):
        municipality = municipality_schema.load(request.get_json())
        municipality.save_to_db()

        return {
            "message": "Municipality created successfully"
        }, 201

   
