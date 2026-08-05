from app.extensions import db
from app.models.category import Category


class CategoryService:

    @staticmethod
    def create_category(data):

        category = Category(
            name=data["name"],
            description=data.get("description")
        )

        db.session.add(category)
        db.session.commit()

        return category

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def update_category(category_id, data):

        category = Category.query.get(category_id)

        if not category:
            return None

        category.name = data.get("name", category.name)
        category.description = data.get(
            "description",
            category.description
        )

        db.session.commit()

        return category

    @staticmethod
    def delete_category(category_id):

        category = Category.query.get(category_id)

        if not category:
            return False

        db.session.delete(category)
        db.session.commit()

        return True
