from fastapi import APIRouter
from sqlmodel import select
from database import SessionDep, Category


router = APIRouter(prefix="/category", tags=["category"])


@router.get("/", response_model=list[Category])
def read_categories(session: SessionDep) -> Category:
    return session.exec(select(Category).order_by(Category.id)).all()