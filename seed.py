import os

import shutil
from pathlib import Path
from tempfile import SpooledTemporaryFile
from fastapi import UploadFile
from sqlmodel import select
from database import get_session, Category, Product, Review


BASE_DIR = Path(__file__).resolve().parent


def base_category_add():
    session = next(get_session())
    
    if session.exec(select(Category)).first():
        return None
    
    pharmacy = Category(title="apteka", text="Аптека")
    feed = Category(title="feed", text="Корм")
    toys = Category(title="toys", text="Игрушки")
    cloth = Category(title="cloth", text="Одежда")
    hygiene = Category(title="hygiene", text="Гигена")

    session.add(pharmacy)
    session.add(feed)
    session.add(toys)
    session.add(cloth)
    session.add(hygiene)

    session.commit()


def base_product_add():
    session = next(get_session())

    if session.exec(select(Product)).first():
        return None
    
    
    def create_upload_file(filepath: str) -> UploadFile:
        if not filepath.exists():
            raise FileNotFoundError(f"Файл {filepath} не найден")
        
        spooled_file = SpooledTemporaryFile(max_size=10 * 1024 * 1024)
        
        with open(filepath, 'rb') as original_file:
            shutil.copyfileobj(original_file, spooled_file)
        
        spooled_file.seek(0)
        
        file_size = os.path.getsize(filepath)
        
        upload_file = UploadFile(
            filename=filepath.name,
            file=spooled_file,
            size=file_size
        )
        
        return upload_file
    
    products = [
        # Аптека
        Product(
            price=758,
            description="Капли от блох и гельминтов для кошек KRKA Селафорт 45мг 0.75мл",
            image=create_upload_file(BASE_DIR / "static/images/products/hit2.png"),
            is_hit=True,
            category_id=1,
            brand="KRKA",
            country="Словения",
            material="Ветеринарный препарат",
            animal_age="Для взрослых кошек"
        ),
        Product(
            price=591,
            description="Антигельминтик для котят и кошек Elanco Мильбемакс мелких пород 2 таблетки",
            image=create_upload_file(BASE_DIR / "static/images/products/tovar3.jpg"),
            is_hit=False,
            category_id=1,
            brand="Elanco",
            country="Франция",
            material="Ветеринарный препарат",
            animal_age="Для котят и мелких кошек"
        ),
        Product(
            price=796,
            description="Антигельминтик для кошек Elanco Дронтал плюс",
            image=create_upload_file(BASE_DIR / "static/images/products/apteka1.png"),
            is_hit=True,
            category_id=1,
            brand="Elanco",
            country="Германия",
            material="Ветеринарный препарат",
            animal_age="Для взрослых кошек"
        ),
        Product(
            price=288,
            description="Таблетки для кошек и собак Apicenna Миртацен для повышения аппетита 1.88мг 10шт",
            image=create_upload_file(BASE_DIR / "static/images/products/apteka2.png"),
            is_hit=False,
            category_id=1,
            brand="Apicenna",
            country="Россия",
            material="Ветеринарный препарат",
            animal_age="Для взрослых кошек"
        ),

        # Корм
        Product(
            price=85,
            description="Корм для кошек ROYAL CANIN 85г Gastrointestinal соус при расстройствах пищеварения",
            image=create_upload_file(BASE_DIR / "static/images/products/hit1.png"),
            is_hit=True,
            category_id=2,
            brand="Royal Canin",
            country="Россия",
            material="Влажный корм",
            animal_age="Для всех возрастов"
        ),
        Product(
            price=89,
            description="Корм влажный для кошек PRO PLAN MAINTENANCE 85 г с курицей в соусе",
            image=create_upload_file(BASE_DIR / "static/images/products/tovar4.png"),
            is_hit=False,
            category_id=2,
            brand="Purina Pro Plan",
            country="Россия",
            material="Влажный корм",
            animal_age="Для стерилизованных кошек"
        ),
        Product(
            price=84,
            description="Корм для котят AWARD 85гр с индейкой healthy growth",
            image=create_upload_file(BASE_DIR / "static/images/products/feed1.png"),
            is_hit=True,
            category_id=2,
            brand="AWARD",
            country="Россия",
            material="Влажный корм",
            animal_age="Для всех возрастов"
        ),
        Product(
            price=84,
            description="Корм влажный для кошек Гурмэ Натуральные рецепты 75г",
            image=create_upload_file(BASE_DIR / "static/images/products/feed2.png"),
            is_hit=False,
            category_id=2,
            brand="Гурмэ",
            country="Россия",
            material="Влажный корм",
            animal_age="Для всех возрастов"
        ),


        # Игрушки
        Product(
            price=315,
            description="Пирамидка для кошек Barbaks Ёлочка-трек 2-слойная интерактивная с шариками голубая",
            image=create_upload_file(BASE_DIR / "static/images/products/hit3.jpg"),
            is_hit=True,
            category_id=3,
            brand="Barbaks",
            country="Китай",
            material="Пластик",
            animal_age="Для всех возрастов"
        ),
        Product(
            price=195,
            description="Игрушка для кошек Barbaks Мятный шар в пластике на липучке 4.5 см",
            image=create_upload_file(BASE_DIR / "static/images/products/tovar2.jpg"),
            is_hit=False,
            category_id=3,
            brand="Barbaks",
            country="Китай",
            material="Пластик, кошачья мята",
            animal_age="Для всех возрастов"
        ),
        Product(
            price=49,
            description="Игрушка для кошек Barbaks Рыба Барбус с кошачьей мятой мягкая 19*11см",
            image=create_upload_file(BASE_DIR / "static/images/products/toys1.png"),
            is_hit=True,
            category_id=3,
            brand="Barbaks",
            country="Китай",
            material="Пластик, кошачья мята",
            animal_age="Для всех возрастов"
        ),
        Product(
            price=89,
            description="Игрушка для кошек Barbaks Рыба Макрель с кошачьей мятой мягкая 19*4.5см",
            image=create_upload_file(BASE_DIR / "static/images/products/toys2.png"),
            is_hit=False,
            category_id=3,
            brand="Barbaks",
            country="Китай",
            material="Пластик, кошачья мята",
            animal_age="Для всех возрастов"
        ),

        # Одежда
        Product(
            price=499,
            description="Джемпер для собак и кошек Zoozavr",
            image=create_upload_file(BASE_DIR / "static/images/products/tovar1.jpg"),
            is_hit=True,
            category_id=4,
            brand="Zoozavr",
            country="Россия",
            material="Трикотаж",
            animal_age="Для взрослых питомцев"
        ),
        Product(
            price=599,
            description="Жилет для кошек PRADA",
            image=create_upload_file(BASE_DIR / "static/images/products/hit4.jpg"),
            is_hit=False,
            category_id=4,
            brand="PRADA",
            country="Италия",
            material="Текстиль",
            animal_age="Для взрослых кошек"
        ),
        Product(
            price=399,
            description="Комбинезон для кошек Зоозавр",
            image=create_upload_file(BASE_DIR / "static/images/products/cloth1.png"),
            is_hit=False,
            category_id=4,
            brand="Зоозавр",
            country="Россия",
            material="Текстиль",
            animal_age="Для взрослых кошек"
        ),
        Product(
            price=3999,
            description="Меховая шуба Balenciaga для кошек",
            image=create_upload_file(BASE_DIR / "static/images/products/cloth2.png"),
            is_hit=False,
            category_id=4,
            brand="Balenciaga",
            country="Испания",
            material="Текстиль",
            animal_age="Для взрослых кошек"
        ),
    ]

    session.add_all(products)
    session.commit()


def base_review_add():
    session = next(get_session())
    
    if session.exec(select(Review)).first():
        return None

    reviews = [
        Review(
            username="Дмитрий",
            email="dmiry23@mail.ru",
            text="Брал игрушки и миску. Качество удивило — всё прочное, ничего не разваливается через неделю. Кот доволен, я тоже. Буду заказывать ещё"
        ),
        Review(
            username="Светлана",
            email="svet343@yandex.ru",
            text="Заказала лежанку для своей кошки — она заняла её в ту же секунду. Материал мягкий, ничего лишнего, цена адекватная. Приятно, что магазин семейный — чувствуется забота."
        ),
        Review(
            username="Анна",
            email="annaJf232@gmail.com",
            text="Очень понравился подход компании. Быстро ответили, помогли выбрать товар. Когтеточка оказалась лучше, чем ожидала — стильная, удобная и не занимает полкомнаты."
        )
    ]

    session.add_all(reviews)
    session.commit()