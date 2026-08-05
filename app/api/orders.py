from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.services.order_service import OrderService

order_bp = Blueprint("orders", __name__)


@order_bp.route("/", methods=["POST"])
@jwt_required()
def create_order():

    data = request.get_json()

    current_user = User.query.get(get_jwt_identity())

    order, error = OrderService.create_order(data, current_user)

    if error:
        return jsonify({"message": error}), 400

    return jsonify(order.to_dict()), 201


@order_bp.route("/", methods=["GET"])
@jwt_required()
def get_orders():

    current_user = User.query.get(get_jwt_identity())

    orders = OrderService.get_all_orders(current_user)

    return jsonify([order.to_dict() for order in orders]), 200


@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):

    current_user = User.query.get(get_jwt_identity())

    order = OrderService.get_order(order_id, current_user)

    if not order:
        return jsonify({"message": "Order not found"}), 404

    return jsonify(order.to_dict()), 200


@order_bp.route("/<int:order_id>", methods=["PUT"])
@jwt_required()
def update_order(order_id):

    data = request.get_json()

    current_user = User.query.get(get_jwt_identity())

    order = OrderService.update_order(
        order_id,
        data,
        current_user
    )

    if not order:
        return jsonify({
            "message": "Order not found or access denied"
        }), 404

    return jsonify(order.to_dict()), 200


@order_bp.route("/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id):

    current_user = User.query.get(get_jwt_identity())

    deleted = OrderService.delete_order(
        order_id,
        current_user
    )

    if not deleted:
        return jsonify({
            "message": "Order not found or access denied"
        }), 404

    return jsonify({
        "message": "Order deleted successfully"
    }), 200
