from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.category_service import CategoryService

category_bp = Blueprint("categories", __name__)


@category_bp.route("", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    response, status = CategoryService.create(data)
    return jsonify(response), status


@category_bp.route("", methods=["GET"])
def get_all():
    response, status = CategoryService.get_all()
    return jsonify(response), status


@category_bp.route("/<int:category_id>", methods=["GET"])
def get_one(category_id):
    response, status = CategoryService.get_by_id(category_id)
    return jsonify(response), status


@category_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
def update(category_id):
    data = request.get_json()
    response, status = CategoryService.update(category_id, data)
    return jsonify(response), status


@category_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete(category_id):
    response, status = CategoryService.delete(category_id)
    return jsonify(response), status
