from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    get_current_user,
)
from marshmallow import ValidationError
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from utils.messages import ERROR_BLANK_FIELD, NOT_FOUND, ERROR_INSERTING

user_schema = UserSchema()
users_schema_list = UserSchema(many=True)


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_email(user.email):
            return {"message": "A user with that email already exists."}, 400

        user.password = generate_password_hash(user.password)

        user.save_to_db()
        message = user.send_email_confirmation()

        return message, 201


class User(Resource):
    @classmethod
    def get(cls, uuid: str):
        user = UserModel.find_by_uuid(uuid)
        if not user:
            return {"message": "User not found."}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        user.delete_from_db()
        return {"message": "User deleted."}, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, uuid: str):
        user = UserModel.find_by_uuid(uuid)

        if not user:
            return {"message": "User not found"}, 404

        user.activated = True
        user.save_to_db()
        return {"message": "User confirmed"}, 200


class Users(Resource):
    @classmethod
    def get(cls):
        return {"users": users_schema_list.dump(UserModel.find_all())}
