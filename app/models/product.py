from datetime import datetime
from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    price = db.Column(db.Float, nullable=False)

    stock = db.Column(db.Integer, default=0)

    image = db.Column(db.String(255))

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
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

    category = db.relationship(
        "Category",
        backref="products"
    )
     
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image": self.image,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()

            }
