from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(db.Integer)

    total_price = db.Column(db.Float)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id")
    )
