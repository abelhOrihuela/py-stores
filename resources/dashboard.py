from flask_restful import Resource
from models.user import UserModel
from models.organization import OrganizationModel
from models.post import PostModel
from flask_jwt_extended import get_current_user, jwt_required


class Dashboard(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        # users = 0
        # organizations = 0
        # posts = 0
        # user = get_current_user()
        # if user.role == "admin":
        # print("***************")
        # print(claims.organizations[0].id)

        users = UserModel.count()
        organizations = OrganizationModel.count()
        posts = PostModel.count()

        return {
            "users": users,
            "organizations": organizations,
            "posts": posts,
        }
