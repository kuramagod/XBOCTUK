from admin.auth import AdminDep
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from database import SessionDep, Review, ReviewCreate, ReviewUpdate


router = APIRouter(prefix="/review", tags=["review"])


@router.get("/", response_model=list[Review])
def read_reviews(session: SessionDep) -> Review:
    return session.exec(select(Review).order_by(Review.id)).all()


@router.post("/", response_model=Review)
def create_product(
    review: ReviewCreate,
    session: SessionDep
    ) -> Review:
    db_item = Review.model_validate(review)
    session.add(db_item)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Нерерная информация")
    
    session.refresh(db_item)
    return db_item


@router.patch("/{review_id}", response_model=Review)
def update_item(
    category_id: int,
    review: ReviewUpdate,
    admin: AdminDep,
    session: SessionDep
    ) -> Review:
    review_db = session.get(Review, category_id)

    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    review_data = review.model_dump(exclude_unset=True)
    review_db.sqlmodel_update(review_data)
    session.add(review_db)
    session.commit()    
    session.refresh(review_db)
    return review_db


@router.delete("/{review_id}")
def delete_item(
    review_id: int,
    admin: AdminDep,
    session: SessionDep
    ) -> dict: 
    category_db = session.get(Review, review_id)

    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    session.delete(category_db)
    session.commit()
    return {"OK": True}