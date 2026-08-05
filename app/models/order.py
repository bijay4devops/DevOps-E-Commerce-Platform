from datetime import datetime
from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    total_price = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="orders"
    )

    product = db.relationship(
        "Product",
        backref="orders"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "status": self.status,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
