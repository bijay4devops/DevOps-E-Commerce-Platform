from flask import Blueprint
from flask import jsonify

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "application": "DevOps E-Commerce Platform",
        "version": "1.0.0"
    })
