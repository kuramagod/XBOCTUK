from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from database import SessionDep, Product, ProductRead, Category


router = APIRouter(prefix="/product", tags=["product"])


@router.get("/", response_model=list[ProductRead])
def read_products(
    session: SessionDep, 
    category: Annotated[str | None, Query(min_length=3)] = None) -> Product:
    query = select(Product)

    if category:
        db_category = session.exec(select(Category).where(Category.title == category)).first()
        if not db_category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Категория не найдена")
        query = query.where(Product.category_id == db_category.id)
    
    query = query.order_by(Product.id)
    results = session.exec(query).all()
    return [
        ProductRead(
            **product.model_dump(exclude=["image"]),
            image=product.image_url,
            category=product.category.text
        ) for product in results
    ]