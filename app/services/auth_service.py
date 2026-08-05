from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import User


class AuthService:

    @staticmethod
    def register(data):

        # Check if username already exists
        if User.query.filter_by(username=data["username"]).first():
            return None, "Username already exists"

        # Check if email already exists
        if User.query.filter_by(email=data["email"]).first():
            return None, "Email already exists"

        # Create new user
        user = User(
            username=data["username"],
            email=data["email"],
            role="customer"
        )

        # Hash password
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return user, None

    @staticmethod
    def login(data):

        user = User.query.filter_by(
            email=data["email"]
        ).first()

        if not user:
            return None

        if not user.check_password(data["password"]):
            return None

        token = create_access_token(
            identity=str(user.id)
        )

        return {
            "token": token,
            "user": user.to_dict()
        }
