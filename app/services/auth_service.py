from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import User


class AuthService:

    @staticmethod
    def register(username, email, password):

        user = User.query.filter_by(email=email).first()

        if user:
            return {"message": "Email already exists"}, 409

        hashed_password = generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return {
            "message": "User registered successfully"
        }, 201

    @staticmethod
    def login(email, password):

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "Invalid credentials"}, 401

        if not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401

        token = create_access_token(identity=str(user.id))

        return {
            "token": token,
            "user": user.to_dict()
        }, 200
