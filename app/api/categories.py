from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.category_service import CategoryService
from app.utils.decorators import admin_required

category_bp = Blueprint("categories", __name__)


# ==========================================
# Create Category (Admin Only)
# ==========================================
@category_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_category():

    data = request.get_json()

    category = CategoryService.create_category(data)

    return jsonify(category.to_dict()), 201


# ==========================================
# Get All Categories (Public)
# ==========================================
@category_bp.route("/", methods=["GET"])
def get_categories():

    categories = CategoryService.get_all_categories()

    return jsonify(
        [category.to_dict() for category in categories]
    ), 200


# ==========================================
# Get Single Category (Public)
# ==========================================
@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):

    category = CategoryService.get_category(category_id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    return jsonify(category.to_dict()), 200


# ==========================================
# Update Category (Admin Only)
# ==========================================
@category_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_category(category_id):

    data = request.get_json()

    category = CategoryService.update_category(
        category_id,
        data
    )

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    return jsonify(category.to_dict()), 200


# ==========================================
# Delete Category (Admin Only)
# ==========================================
@category_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_category(category_id):

    deleted = CategoryService.delete_category(category_id)

    if not deleted:
        return jsonify({
            "message": "Category not found"
        }), 404

    return jsonify({
        "message": "Category deleted successfully"
    }), 200
