from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from ma import ma
from db import db
from blacklist import BLACKLIST
from resources.user import (
    UserRegister,
    UserLogin,
    User,
    UserMe,
    TokenRefresh,
    UserLogout,
    UserConfirm,
)
from resources.organizations import Organizations, Organization, OrganizationUsers
from marshmallow import ValidationError
from flask_migrate import Migrate

DB_URL = "postgresql+psycopg2://localhost:5432/test"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens

app.secret_key = "ABELORIHUELA"  # could do app.config['JWT_SECRET_KEY'] if we prefer
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


api.add_resource(Organizations, "/organizations")
api.add_resource(Organization, "/organizations/<string:uuid>")
api.add_resource(OrganizationUsers, "/organizations/<string:org>/users/<string:user>")

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
