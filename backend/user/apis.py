from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import DecodeError
from user.models import User
from db import db

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_user_profile():
    try:
        # Extract user ID from the JWT token
        current_user_id = get_jwt_identity()

        # Retrieve user and user tweets from the database
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"error": "User not found!"}), 404

        return {
            'id': user.id,
            'username': user.username,
            'bio': user.bio,
        }

    except NoAuthorizationError:
        # Handle the case when the JWT token is missing
        return jsonify({"error_message": "Token tidak ditemukan"}), 401

    except (DecodeError, Exception) as e:
        print(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500