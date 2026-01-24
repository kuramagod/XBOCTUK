from admin.auth import AdminDep
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from database import SessionDep, Category, CategoryCreate, CategoryUpdate


router = APIRouter(prefix="/category", tags=["category"])


@router.get("/", response_model=list[Category])
def read_categories(session: SessionDep) -> Category:
    return session.exec(select(Category).order_by(Category.id)).all()


@router.post("/", response_model=Category)
def create_product(
    category: CategoryCreate,
    admin: AdminDep,
    session: SessionDep
    ) -> Category:
    db_item = Category.model_validate(category)
    session.add(db_item)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Нерерная информация")
    
    session.refresh(db_item)
    return db_item


@router.patch("/{category_id}", response_model=Category)
def update_item(
    category_id: int,
    admin: AdminDep,
    category: CategoryUpdate,
    session: SessionDep
    ) -> Category:
    category_db = session.get(Category, category_id)

    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    category_data = category.model_dump(exclude_unset=True)
    category_db.sqlmodel_update(category_data)
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return category_db


@router.delete("/{category_id}")
def delete_item(
    category_id: int,
    admin: AdminDep,
    session: SessionDep
    ) -> dict: 
    category_db = session.get(Category, category_id)

    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    session.delete(category_db)
    session.commit()
    return {"OK": True}