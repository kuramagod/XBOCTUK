from pathlib import Path
from random import sample

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from sqladmin import Admin

from admin.auth import AdminAuth
from admin.views import CategoryAdmin, ProductAdmin, ReviewAdmin
from core.config import SECRET_KEY
from core.security import create_super_user
from database import create_dn_and_tables, SessionDep, Product, engine
from routers import product, review, category, user
from seed import base_category_add, base_product_add, base_review_add


app = FastAPI()

app.include_router(product.router, prefix="/api")
app.include_router(review.router, prefix="/api")
app.include_router(category.router, prefix="/api")
app.include_router(user.router, prefix="/api")

admin = Admin(
    app, 
    engine, 
    authentication_backend=AdminAuth(secret_key=SECRET_KEY)
)

admin.add_view(CategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ReviewAdmin)

BASE_DIR = Path(__file__).resolve().parent
template_obj = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.on_event("startup")
def on_startup():
    create_dn_and_tables()
    create_super_user()

    # Заполнение демо-данными
    base_category_add()
    base_product_add()
    base_review_add()


@app.get("/")
def main_page(
    request: Request,
    session: SessionDep
    ):
    reviews = review.read_reviews(session)[-3:]
    categories = category.read_categories(session)
    hits = session.exec(select(Product).where(Product.is_hit == True)).all()
    hit_products = sample(hits, 4) if len(hits) >= 4 else hits

    return template_obj.TemplateResponse("index.html", {
        "request": request, 
        "reviews": reviews, 
        "categories": categories,
        "hit_products": hit_products
    })
