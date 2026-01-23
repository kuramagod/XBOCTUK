from sqlmodel import Session, select
from database import engine, Category, Product, Review


def base_category_add():
    with Session(engine) as session:
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
    with Session(engine) as session:
        if session.exec(select(Product)).first():
            return None
        
        products = [
            # Аптека
            Product(
                price=758,
                description="Капли от блох и гельминтов для кошек KRKA Селафорт 45мг 0.75мл",
                image="products/hit2.png",
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
                image="products/tovar3.jpg",
                is_hit=False,
                category_id=1,
                brand="Elanco",
                country="Франция",
                material="Ветеринарный препарат",
                animal_age="Для котят и мелких кошек"
            ),

            # Корм
            Product(
                price=85,
                description="Корм для кошек ROYAL CANIN 85г Gastrointestinal соус при расстройствах пищеварения",
                image="products/hit1.png",
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
                image="products/tovar4.png",
                is_hit=False,
                category_id=2,
                brand="Purina Pro Plan",
                country="Россия",
                material="Влажный корм",
                animal_age="Для стерилизованных кошек"
            ),

            # Игрушки
            Product(
                price=315,
                description="Пирамидка для кошек Barbaks Ёлочка-трек 2-слойная интерактивная с шариками голубая",
                image="products/hit3.jpg",
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
                image="products/tovar2.jpg",
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
                image="products/tovar1.jpg",
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
                image="products/hit4.jpg",
                is_hit=False,
                category_id=4,
                brand="PRADA",
                country="Италия",
                material="Текстиль",
                animal_age="Для взрослых кошек"
            ),
        ]

        session.add_all(products)
        session.commit()


def base_review_add():
    with Session(engine) as session:
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