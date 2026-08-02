import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
        f"{os.getenv('MYSQL_PASSWORD')}@"
        f"{os.getenv('MYSQL_HOST')}:"
        f"{os.getenv('MYSQL_PORT')}/"
        f"{os.getenv('MYSQL_DATABASE')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
