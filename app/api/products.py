from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.product_service import ProductService
from app.utils.decorators import admin_required

product_bp = Blueprint("products", __name__)


# ==========================================
# Create Product (Admin Only)
# ==========================================
@product_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_product():

    data = request.get_json()

    product = ProductService.create_product(data)

    return jsonify(product.to_dict()), 201


# ==========================================
# Get All Products (Public)
# ==========================================
@product_bp.route("/", methods=["GET"])
def get_products():

    products = ProductService.get_all_products()

    return jsonify(
        [product.to_dict() for product in products]
    ), 200


# ==========================================
# Get Single Product (Public)
# ==========================================
@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):

    product = ProductService.get_product(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(product.to_dict()), 200


# ==========================================
# Update Product (Admin Only)
# ==========================================
@product_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_product(product_id):

    data = request.get_json()

    product = ProductService.update_product(
        product_id,
        data
    )

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(product.to_dict()), 200


# ==========================================
# Delete Product (Admin Only)
# ==========================================
@product_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_product(product_id):

    deleted = ProductService.delete_product(product_id)

    if not deleted:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify({
        "message": "Product deleted successfully"
    }), 200
