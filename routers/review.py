from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from database import SessionDep, Review, ReviewCreate


router = APIRouter(prefix="/review", tags=["review"])


@router.get("/", response_model=list[Review])
def read_reviews(session: SessionDep) -> Review:
    return session.exec(select(Review).order_by(Review.id.desc())).all()


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