from decimal import Decimal
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship, select


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connection_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connection_args)


def create_dn_and_tables():
    SQLModel.metadata.create_all(engine)


def base_category_add():
    with Session(engine) as session:
        if session.exec(select(Category)).first():
            return None
        
        pharmacy = Category(id=1, title="apteka", text="Аптека")
        feed = Category(id=2, title="feed", text="Корм")
        toys = Category(id=3, title="toys", text="Игрушки")
        cloth = Category(id=4, title="cloth", text="Одежда")
        hygiene = Category(id=5, title="hygiene", text="Гигена")

        session.add(pharmacy)
        session.add(feed)
        session.add(toys)
        session.add(cloth)
        session.add(hygiene)

        session.commit()

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Модели
# JWT-Токен
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


# Админ
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    is_admin: bool


# Категории
class CategoryBase(SQLModel):
    title: str
    text: str


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    products: list["Product"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    title: str | None = None
    text: str | None = None

# Товары
class ProductBase(SQLModel):
    description: str
    is_hit: bool = False
    brand: str | None = None
    country: str | None = None
    material: str | None = None
    animal_age: str | None = None
    image: str | None = None


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    price: Decimal  
    category_id: int | None = Field(default=None, foreign_key="category.id")
    category: Category | None = Relationship(back_populates="products")


class ProductCreate(ProductBase):
    price: Decimal
    image: str | None = None
    category_id: int


class ProductRead(SQLModel):
    id: int
    price: Decimal
    description: str
    image: str
    brand: str | None
    country: str | None
    material: str | None
    animal_age: str | None
    category: str


class ProductUpdate(SQLModel):
    price: Decimal | None = None
    description: str | None = None
    is_hit: bool | None = None
    brand: str | None = None
    country: str | None = None
    material: str | None = None
    animal_age: str | None = None

# Отзывы
class ReviewBase(SQLModel):
    username: str
    email: str
    text: str


class Review(ReviewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    text: str | None = None