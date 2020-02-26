from flask_restful import Resource
from schemas.project import ProjectSchema
from models.project import ProjectModel
from flask import request

projects_schema = ProjectSchema()
projects_list_schema = ProjectSchema(many=True)


class Project(Resource):
    @classmethod
    def get(cls, uuid: str):

        project = ProjectModel.find_by_uuid(uuid)

        return projects_schema.dump(project), 200

    @classmethod
    def put(cls, uuid: str):
        project_request = projects_schema.load(request.get_json())

        project = ProjectModel.find_by_uuid(uuid)

        if not project:
            return {"message": "Project not found"}, 404

        project.name = project_request.name
        project.type = project_request.type
        project.status = project_request.status

        project.save_to_db()

        return {"message": "Project updated"}, 200

    @classmethod
    def delete(cls, uuid: str):
        project = ProjectModel.find_by_uuid(uuid)
        if not project:
            return {"message": "Project not found."}, 404
        project.delete_from_db()
        return {"message": "Project deleted."}, 200


class Projects(Resource):
    @classmethod
    def get(cls):
        return {"projects": projects_list_schema.dump(ProjectModel.find_all())}, 200

    @classmethod
    def post(cls):

        project_request = projects_schema.load(request.get_json())

        project_request.save_to_db()

        return {"message": "Project created successfully"}, 201
