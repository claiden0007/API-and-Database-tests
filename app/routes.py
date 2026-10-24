
from flask import Blueprint, current_app, jsonify, request
import sqlite3

from app.database import (
    create_users_table,
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
)

users_bp = Blueprint("users", __name__)


def get_database_path():
    return current_app.config["DATABASE"]


@users_bp.route("/users", methods=["POST"])
def create_user_endpoint():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({"error": "Email is required"}), 400

    if isinstance(age, bool) or not isinstance(age, int) or age < 18:
        return jsonify({"error": "Age must be an integer of at least 18"}), 400

    try:
        user_id = create_user(
            get_database_path(), name.strip(), email.strip(), age
        )
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists or data is invalid"}), 409

    return jsonify({
        "id": user_id,
        "name": name.strip(),
        "email": email.strip(),
        "age": age,
    }), 201


@users_bp.route("/users", methods=["GET"])
def list_users_endpoint():
    users = get_all_users(get_database_path())
    return jsonify(users), 200


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_endpoint(user_id):
    user = get_user(get_database_path(), user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_endpoint(user_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({"error": "Email is required"}), 400

    if isinstance(age, bool) or not isinstance(age, int) or age < 18:
        return jsonify({"error": "Age must be an integer of at least 18"}), 400

    database_path = get_database_path()

    if get_user(database_path, user_id) is None:
        return jsonify({"error": "User not found"}), 404

    try:
        update_user(database_path, user_id, name.strip(), email.strip(), age)
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists or data is invalid"}), 409

    return jsonify(get_user(database_path, user_id)), 200


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_endpoint(user_id):
    deleted = delete_user(get_database_path(), user_id)

    if not deleted:
        return jsonify({"error": "User not found"}), 404

    return "", 204
