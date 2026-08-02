from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    description = db.Column(db.Text)

    price = db.Column(db.Float)

    stock = db.Column(db.Integer)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id")
    )
