from pathlib import Path
import shutil
import uuid
from sqladmin import ModelView
from sqladmin.fields import FileField
from markupsafe import Markup
from database import Category, Review, Product



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

    UPLOAD_PATH = Path("static/images/products")
    BASE_STATIC_URL = "/static/images/"

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

    column_formatters = {
        Product.price: lambda m, a: f"{round(m.price)} ₽",
        Product.description: lambda m, a: (
            m.description[:40] + "..." if m.description else ""
        ),
        Product.image: lambda m, a: (
            Markup(
                f'<img src="{ProductAdmin.BASE_STATIC_URL}{m.image}" '
                f'style="max-height:100px; max-width:100px; border-radius:6px;">'
            )
            if m.image else "Нет изображения"
        ),
    }

    column_formatters_detail = {
        Product.image: lambda m, a: (
            Markup(
                f'<img src="{ProductAdmin.BASE_STATIC_URL}{m.image}" '
                f'style="max-height:100px; max-width:100px; border-radius:6px;">'
            )
            if m.image else "Нет изображения"
        ),
    }

    form_overrides = {
        "image": FileField
    }

    async def on_model_change(self, data, model, is_created, request=None):
        file = data.get("image")

        if file:
            self.UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

            ext = Path(file.filename).suffix
            filename = f"{uuid.uuid4().hex}{ext}"
            file_path = self.UPLOAD_PATH / filename

            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            model.image = f"products/{filename}"

            data.pop("image", None)


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