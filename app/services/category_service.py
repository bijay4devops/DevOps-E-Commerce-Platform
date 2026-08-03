from app.extensions import db
from app.models.category import Category


class CategoryService:

    @staticmethod
    def create(data):
        category = Category(
            name=data["name"],
            description=data.get("description")
        )

        db.session.add(category)
        db.session.commit()

        return category.to_dict(), 201

    @staticmethod
    def get_all():
        categories = Category.query.all()
        return [c.to_dict() for c in categories], 200

    @staticmethod
    def get_by_id(category_id):
        category = Category.query.get_or_404(category_id)
        return category.to_dict(), 200

    @staticmethod
    def update(category_id, data):
        category = Category.query.get_or_404(category_id)

        category.name = data["name"]
        category.description = data.get("description")

        db.session.commit()

        return category.to_dict(), 200

    @staticmethod
    def delete(category_id):
        category = Category.query.get_or_404(category_id)

        db.session.delete(category)
        db.session.commit()

        return {"message": "Category deleted"}, 200
