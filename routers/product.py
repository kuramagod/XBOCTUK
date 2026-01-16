from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from database import SessionDep, Product, ProductCreate, ProductUpdate, Category


router = APIRouter(prefix="/product", tags=["product"])


@router.get("/", response_model=list[Product])
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


@router.post("/", response_model=Product)
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


@router.patch("/{product_id}", response_model=Product)
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


@router.delete("/{product_id}")
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