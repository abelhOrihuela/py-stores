from flask_restful import Resource
from schemas.post import PostSchema
from models.post import PostModel
from flask import request

post_schema = PostSchema()
post_schema_list = PostSchema(many=True)


class Post(Resource):
    @classmethod
    def get(cls, uuid: str):
        post = PostModel.find_by_uuid(uuid)

        if not post:
            return {"message": "Project not found."}, 404

        return post_schema.dump(post), 200

    @classmethod
    def put(cls, uuid: str):
        post_request = post_schema.load(request.get_json())

        post = PostModel.find_by_uuid(uuid)

        if not post:
            return {"message": "Post not found."}, 404

        post.title = post_request.title
        post.subtitle = post_request.subtitle
        post.tags = post_request.tags
        post.content = post_request.content
        post.author = post_request.author

        post.save_to_db()

        return {"message": "Post updated."}, 200

    @classmethod
    def delete(cls, uuid: str):

        post = PostModel.find_by_uuid(uuid)

        if not post:
            return {"message": "Post not found."}, 404

        post.delete_from_db()

        return {"message": "Post deleted."}


class Posts(Resource):
    @classmethod
    def get(cls):
        return {"posts": post_schema_list.load(PostModel.find_all())}, 200

    @classmethod
    def post(cls):
        post_request = post_schema.load(request.get_json())

        post_request.save_to_db()

        return {"message": "Post created."}
