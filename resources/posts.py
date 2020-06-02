from flask_restful import Resource
from schemas.post import PostSchema
from models.post import PostModel
from models.organization import OrganizationModel
from flask import request, session, g
from flask_jwt_extended import get_current_user, jwt_required

post_schema = PostSchema()
post_schema_list = PostSchema(many=True)


class Post(Resource):
    @classmethod
    def get(cls, org: str, uuid: str):
        post = PostModel.find_by_uuid(uuid)

        if not post:
            return {"message": "Project not found."}, 404

        return post_schema.dump(post), 200

    @classmethod
    @jwt_required
    def put(cls, org: str, post: str):

        user = get_current_user()
        organization = OrganizationModel.find_by_uuid(org)

        request_json = request.get_json()
        request_json["user_id"] = user.id
        request_json["organization_id"] = organization.id

        # post_request = post_schema.load(request_json)

        post = PostModel.find_by_uuid(post)

        if not post:
            return {"message": "Post not found."}, 404

        post.title = request_json["title"]
        post.subtitle = request_json["subtitle"]
        post.tags = request_json["tags"]
        post.content = request_json["content"]

        post.save_to_db()

        return {"message": "Post updated."}, 200

    @classmethod
    @jwt_required
    def delete(cls, org: str, post: str):

        post = PostModel.find_by_uuid(post)

        if not post:
            return {"message": "Post not found."}, 404

        post.delete_from_db()

        return {"message": "Post deleted."}


class Posts(Resource):
    @classmethod
    @jwt_required
    def get(cls, org: str):
        organization = OrganizationModel.find_by_uuid(org)

        print(organization.uuid)
        return (
            {"posts": post_schema_list.dump(PostModel.find_by_org(organization.id))},
            200,
        )

    @classmethod
    @jwt_required
    def post(cls, org: str):

        user = get_current_user()
        organization = OrganizationModel.find_by_uuid(org)

        request_json = request.get_json()
        request_json["user_id"] = user.id
        request_json["organization_id"] = organization.id

        post_request = post_schema.load(request_json)
        post_request.save_to_db()

        return {"message": "Post created."}
