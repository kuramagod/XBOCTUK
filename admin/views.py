from sqladmin import ModelView
from sqladmin.fields import FileField
from database import Category, Review, Product


class CategoryAdmin(ModelView, model=Category):
    column_list = [
        Category.id,
        Category.title,
        Category.text
    ]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.price,
        Product.description,
        Product.is_hit,
        Product.image,
        Product.category,
    ]

    column_formatters = {
        Product.price: lambda m, a: f"{round(m.price)} ₽",
        Product.description: lambda m, a: (
            m.description[:50] + "..." if m.description else ""
        ),
    }

    form_columns = [
        Product.price,
        Product.description,
        Product.brand,
        Product.country,
        Product.is_hit,
        Product.material,
        Product.animal_age,
        Product.category,
        Product.image,
    ]

    # form_overrides = {
    #     "image": FileField
    # }

    # form_args = {
    #     "image": {
    #         "label": "Изображение",
    #         # "base_path": "static/images/products",
    #     }
    # }


class ReviewAdmin(ModelView, model=Review):
    column_list = [
        Review.id,
        Review.username,
        Review.text
    ]

    can_create = False