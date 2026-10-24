
import os

from flask import Flask
from app.database import create_users_table
from app.routes import users_bp


def create_app(database_path=None):
    app = Flask(__name__)

    if database_path is None:
        database_path = os.path.join(app.instance_path, "users.db")

    os.makedirs(
        os.path.dirname(os.path.abspath(database_path)),
        exist_ok=True,
    )

    app.config["DATABASE"] = database_path

    create_users_table(database_path)
    app.register_blueprint(users_bp)

    return app
