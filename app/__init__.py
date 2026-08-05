from flask import Flask

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

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
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

    return app
