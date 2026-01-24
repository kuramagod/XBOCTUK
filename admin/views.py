from pathlib import Path
import shutil
import uuid
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
    UPLOAD_PATH = Path("static/images/products")

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
    column_list = [
        Review.id,
        Review.username,
        Review.text
    ]

    can_create = False