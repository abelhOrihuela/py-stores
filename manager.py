from flask import Flask, jsonify
from db import db
import datetime
from instance.config import app_config
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError
from blacklist import BLACKLIST
from models.user import UserModel
from initialize_routes import initialize_routes


DB_URL = "postgresql+psycopg2://localhost:5432/test"


def create_app(environment):
    print("* Running in mode: " + environment)

    app = Flask(__name__, template_folder="emails")

    app.config.from_object(app_config[environment])

    app.app_context().push()
    CORS(app)
    api = Api(app, prefix="/api/v1")
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(error):
        return jsonify(error.messages), 400

    # This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return (
            decrypted_token["jti"] in BLACKLIST
        )  # Here we blacklist particular JWTs that have been created in the past.

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        return UserModel.find_by_id(identity)

    # Routes
    initialize_routes(api)
   
    # app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["PROPAGATE_EXCEPTIONS"] = True
    # app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
    # app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(
    #     days=1
    # )  # enable blacklist feature
    # app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    #     "access",
    #     "refresh",
    # ]  # allow blacklisting for access and refresh tokens

    # app.secret_key = (
    #     "ABELORIHUELA"  # could do app.config['JWT_SECRET_KEY'] if we prefer
    # )

    db.init_app(app)
    return app
