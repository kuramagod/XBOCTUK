from pathlib import Path
from sqladmin import ModelView
from markupsafe import Markup
from database import Category, Review, Product, BASE_DIR


class CategoryAdmin(ModelView, model=Category):
    name = "Категория"
    name_plural = "Категории"

    column_list = [
        Category.id,
        Category.title,
        Category.text
    ]


class ProductAdmin(ModelView, model=Product):
    name = "Товар"
    name_plural = "Товары"

    BASE_STATIC_URL = "/static"

    column_list = [
        Product.id,
        Product.price,
        Product.description,
        Product.is_hit,
        Product.image,
        Product.category,
    ]

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

    def image_formatter(model, attr):
        if not model.image:
            return "Нет изображения"

        path = Path(model.image)
        
        relative = path.relative_to(BASE_DIR / "static")

        return Markup(
            f'<img src="{ProductAdmin.BASE_STATIC_URL}/{relative.as_posix()}" '
            f'style="max-height:100px; border-radius:10px;">'
        )

    column_formatters = {
        Product.price: lambda m, a: f"{round(m.price)} ₽",
        Product.description: lambda m, a: (
            m.description[:40] + "..." if m.description else ""
        ),
        Product.image: image_formatter
    }

    column_formatters_detail = {
        Product.image: image_formatter
    }


class ReviewAdmin(ModelView, model=Review):
    name = "Отзыв"
    name_plural = "Отзывы"

    column_list = [
        Review.id,
        Review.username,
        Review.text
    ]

    column_formatters = {
        Review.text: lambda m, a: (
            m.text[:60] + "..." if m.text else ""
        ),
    }

    can_create = False