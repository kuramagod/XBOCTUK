from pathlib import Path
from random import sample
from fastapi import FastAPI, Request
from sqlmodel import select
from routers import product, review, category
from database import create_dn_and_tables, SessionDep, Product
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.include_router(product.router)
app.include_router(review.router)
app.include_router(category.router)


top = Path(__file__).resolve().parent
template_obj = Jinja2Templates(directory=f"{top}/templates")
app.mount("/static", StaticFiles(directory=f"{top}/static"), name="static")

@app.on_event("startup")
def on_startup():
    create_dn_and_tables()

@app.get("/")
def main_page(
    request: Request,
    session: SessionDep
    ):
    reviews = review.read_reviews(session)
    categories = category.read_categories(session)
    # hits = session.exec(select(Product).where(Product.is_hit == True)).all()
    # hit_products = sample(hits, 4) if len(hits) >= 4 else hits

    return template_obj.TemplateResponse("index.html", {
        "request": request, 
        "reviews": reviews, 
        "categories": categories,
        # "hit_products": hit_products
        })
