from flask_restful import Resource
from models.source import SourceModel
from schemas.source import SourceSchema
from flask import request

source_schema = SourceSchema()
source_list_schema = SourceSchema(many=True)


class Source(Resource):
    @classmethod
    def get(cls, uuid: str):
        source = SourceModel.find_by_uuid(uuid)

        if not source:
            return {"message": "Source not found"}, 404

        return source

    @classmethod
    def put(cls, uuid: str):
        source = SourceModel.find_by_uuid(uuid)
        source_json = request.get_json()
        source_request = source_schema.load(source_json)

        if not source:
            return {"message": "Source not found"}, 404

        source.name = source_json["name"]
        source.site = source_json["site"]
        source.title_selector = source_json["title_selector"]
        source.subtitle_selector = source_json["subtitle_selector"]
        source.content_selector = source_json["content_selector"]
        source.tags_selector = source_json["tags_selector"]
        source.author_selector = source_json["author_selector"]
        source.save_to_db()

        return {"message": "Source updated successfully"}, 200

    @classmethod
    def delete(cls, uuid: str):
        source = SourceModel.find_by_uuid(uuid)

        if not source:
            return {"message": "Source not found"}, 404

        source.delete_from_db()
        return {"message": "Source deleted."}, 200


class Sources(Resource):
    @classmethod
    def post(cls):
        source_request = source_schema.load(request.get_json())
        source_request.save_to_db()

        return {"message": "Source created successfully"}, 201

    @classmethod
    def get(cls):
        return {"sources": source_list_schema.dump(SourceModel.find_all())}
