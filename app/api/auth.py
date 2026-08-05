from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "application": "DevOps E-Commerce Platform",
        "version": "1.0.0"
    })


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    user, error = AuthService.register(data)

    if error:
        return jsonify({
            "message": error
        }), 400

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    result = AuthService.login(data)

    if not result:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    return jsonify(result), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    return jsonify({
        "logged_in_user": get_jwt_identity()
    }), 200
