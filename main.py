from typing import Annotated
from pathlib import Path
from fastapi import FastAPI, Request, Query, HTTPException, status, Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from database import create_dn_and_tables, Product, ProductUpdate, ProductCreate, Category, Review, get_session, Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()


top = Path(__file__).resolve().parent
template_obj = Jinja2Templates(directory=f"{top}/templates")
app.mount("/static", StaticFiles(directory=f"{top}/static"), name="static")
SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_dn_and_tables()

@app.get("/")
def main_page(request: Request):
    return template_obj.TemplateResponse("index.html", {"request": request})


# Товары endpoints
@app.get("/product/", tags=["product"], response_model=list[Product])
def read_products(
    session: SessionDep, 
    category: Annotated[str | None, Query(min_length=3)] = None) -> Product:
    query = select(Product)

    if category:
        db_category = session.exec(select(Category).where(Category.name == category)).first()
        if not db_category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Категория не найдена")
        query = query.where(Product.category_id == db_category.id)
    
    query = query.order_by(Product.id)
    return session.exec(query).all()


@app.post("/product/", tags=["product"], response_model=Product)
def create_product(
    product: ProductCreate,
    session: SessionDep
    ) -> Product:
    db_item = Product.model_validate(product)
    session.add(db_item)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Нерерная информация")
    
    session.refresh(db_item)
    return db_item


@app.patch("/product/{product_id}", tags=["product"], response_model=Product)
def update_item(
    product_id: int,
    product: ProductUpdate,
    session: SessionDep
    ) -> Product:
    product_db = session.get(Product, product_id)

    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    product_data = product.model_dump(exclude_unset=True)
    product_db.sqlmodel_update(product_data)
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db


@app.delete("/product/{product_id}", tags=["product"])
def delete_item(
    product_id: int,
    session: SessionDep
    ) -> dict: 
    product_db = session.get(Product, product_id)

    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    session.delete(product_db)
    session.commit()
    return {"OK": True}