from app.extensions import db
from app.models.order import Order
from app.models.product import Product


class OrderService:

    @staticmethod
    def create_order(data, current_user):

        product = Product.query.get(data["product_id"])

        if not product:
            return None, "Product not found"

        quantity = data["quantity"]

        if product.stock < quantity:
            return None, "Insufficient stock"

        total_price = product.price * quantity

        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            quantity=quantity,
            total_price=total_price,
            status="Pending"
        )

        product.stock -= quantity

        db.session.add(order)
        db.session.commit()

        return order, None

    @staticmethod
    def get_all_orders(current_user):

        if current_user.role == "admin":
            return Order.query.all()

        return Order.query.filter_by(
            user_id=current_user.id
        ).all()

    @staticmethod
    def get_order(order_id, current_user):

        order = Order.query.get(order_id)

        if not order:
            return None

        if current_user.role != "admin" and order.user_id != current_user.id:
            return None

        return order

    @staticmethod
    def update_order(order_id, data, current_user):

        order = Order.query.get(order_id)

        if not order:
            return None

        if current_user.role != "admin" and order.user_id != current_user.id:
            return None

        if "quantity" in data:

            product = Product.query.get(order.product_id)

            difference = data["quantity"] - order.quantity

            if product.stock < difference:
                return None

            product.stock -= difference

            order.quantity = data["quantity"]
            order.total_price = order.quantity * product.price

        if "status" in data:
            order.status = data["status"]

        db.session.commit()

        return order

    @staticmethod
    def delete_order(order_id, current_user):

        order = Order.query.get(order_id)

        if not order:
            return False

        if current_user.role != "admin" and order.user_id != current_user.id:
            return False

        product = Product.query.get(order.product_id)

        if product:
            product.stock += order.quantity

        db.session.delete(order)
        db.session.commit()

        return True
