from pathlib import Path
from fastapi import FastAPI, Request
from routers import product, review, category
from database import create_dn_and_tables, SessionDep
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
    
    return template_obj.TemplateResponse("index.html", {"request": request, "reviews": reviews})
