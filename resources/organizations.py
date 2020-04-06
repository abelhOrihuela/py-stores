from flask_restful import Resource
from flask import request
from models.organization import OrganizationModel
from models.user import UserModel
from schemas.organization import OrganizationSchema

organization_schema = OrganizationSchema()
organization_list_schema = OrganizationSchema(many=True)


class Organizations(Resource):
    # return all
    @classmethod
    def get(cls):
        return {
            "organizations": organization_list_schema.dump(OrganizationModel.find_all())
        }

    # create new
    @classmethod
    def post(cls):
        organization = organization_schema.load(request.get_json())

        if OrganizationModel.find_by_name(organization.name):
            return {"message": "A organization with that name already exists."}, 400

        organization.save_to_db()

        return {"message": "Organization created successfully."}, 201


class Organization(Resource):

    # return by uuid
    @classmethod
    def get(cls, uuid: str):
        org = OrganizationModel.find_by_uuid(uuid)

        if not org:
            return {"message": "Organization not found."}, 404

        return organization_schema.dump(org)

    # update by uuid
    @classmethod
    def put(cls, uuid: str):
        org_request = organization_schema.load(request.get_json())
        org = OrganizationModel.find_by_uuid(uuid)

        if not org:
            return {"message": "Organization not found."}, 404

        org.name = org_request.name
        org_request.save_to_db()

        return organization_schema.dump(org_request), 200

    # delete by uuid
    @classmethod
    def delete(cls, uuid: str):
        return "Hola"


class OrganizationUsers(Resource):
    @classmethod
    def post(cls, org: str, user: str):

        organization = OrganizationModel.find_by_uuid(org)
        member = UserModel.find_by_uuid(user)

        if not organization:
            return {"message": "Organization not found."}, 404

        if not member:
            return {"message": "Organization not found."}, 404

        organization.users.append(member)
        organization.save_to_db()

        return user
