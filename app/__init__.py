from flask import Flask, jsonify

from app.config import Config
from app.extensions import db, migrate, jwt, bcrypt

# Import models
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order

# Import blueprints
from app.api.auth import auth_bp
from app.api.categories import category_bp
from app.api.products import product_bp
from app.api.orders import order_bp


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        category_bp,
        url_prefix="/api/categories"
    )

    app.register_blueprint(
        product_bp,
        url_prefix="/api/products"
    )

    app.register_blueprint(
        order_bp,
        url_prefix="/api/orders"
    )

    # Root Endpoint
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "application": "DevOps E-Commerce Platform",
            "status": "UP",
            "version": "1.0.0",
            "message": "Welcome to the DevOps E-Commerce REST API",
            "endpoints": {
                "health": "/api/auth/health",
                "auth": "/api/auth",
                "products": "/api/products",
                "categories": "/api/categories",
                "orders": "/api/orders"
            }
        }), 200

    # Health Check
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy"
        }), 200

    # 404 Error Handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Resource not found"
        }), 404

    # 500 Error Handler
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error"
        }), 500

    return app
