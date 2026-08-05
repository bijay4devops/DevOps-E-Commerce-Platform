from app.extensions import db
from app.models.product import Product


class ProductService:

    @staticmethod
    def create_product(data):
        product = Product(
            name=data["name"],
            description=data.get("description"),
            price=data["price"],
            stock=data.get("stock", 0),
            image=data.get("image"),
            category_id=data["category_id"]
        )

        db.session.add(product)
        db.session.commit()

        return product

    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def get_product(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)

        if not product:
            return None

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.stock = data.get("stock", product.stock)
        product.image = data.get("image", product.image)
        product.category_id = data.get("category_id", product.category_id)

        db.session.commit()

        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)

        if not product:
            return False

        db.session.delete(product)
        db.session.commit()

        return True
