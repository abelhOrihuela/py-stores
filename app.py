from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from ma import ma
from db import db
from blacklist import BLACKLIST
from marshmallow import ValidationError
from flask_migrate import Migrate
from sa import create_app

# Resources
from resources.users import UserRegister, User, UserConfirm
from resources.login import UserLogin, UserMe, TokenRefresh, UserLogout
from resources.organizations import Organizations, Organization, OrganizationUsers
from resources.sources import Source, Sources
from resources.states import State, States
from resources.posts import Posts


app = create_app()
app.app_context().push()

api = Api(app, prefix="/api")
jwt = JWTManager(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(error):
    return jsonify(error.messages), 400


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
        decrypted_token["jti"] in BLACKLIST
    )  # Here we blacklist particular JWTs that have been created in the past.


# Routes

# get list & create
api.add_resource(Organizations, "/organizations")
# get, update, delete by uuid
api.add_resource(Organization, "/organizations/<string:uuid>")

api.add_resource(OrganizationUsers, "/organizations/<string:org>/users/<string:user>")

api.add_resource(Source, "/sources/<string:uuid>")
api.add_resource(Sources, "/sources")

api.add_resource(State, "/states/<string:uuid>")
api.add_resource(States, "/states")

api.add_resource(Posts, "/posts")

api.add_resource(UserRegister, "/register")
api.add_resource(UserConfirm, "/user-confirm/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserMe, "/me")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
