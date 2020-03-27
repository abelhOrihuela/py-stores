from flask import Flask
from db import db

DB_URL = "postgresql+psycopg2://localhost:5432/test"


def create_app():
    app = Flask(__name__, template_folder="emails")

    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
        "access",
        "refresh",
    ]  # allow blacklisting for access and refresh tokens

    app.secret_key = (
        "ABELORIHUELA"  # could do app.config['JWT_SECRET_KEY'] if we prefer
    )

    db.init_app(app)
    return app
