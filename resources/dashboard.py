from flask_restful import Resource
from models.organization import OrganizationModel
from models.post import PostModel
from flask_jwt_extended import get_current_user, jwt_required


class Dashboard(Resource):
    @classmethod
    @jwt_required
    def get(cls, org: str):

        organization = OrganizationModel.find_by_uuid(org)
        posts = PostModel.count_by_org(organization.id)

        return {
            "users": len(organization.users),
            "posts": posts,
        }
