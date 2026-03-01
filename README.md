# Хвостик 🐱

Веб-сайт для семейного магазина товаров для кошек с административной панелью и REST API.

> **Слоган:** Лучшее проявление любви к любимцу!

## 📋 Описание

Одностраничный сайт-визитка с полноценным backend на FastAPI. Проект включает информационные разделы о компании, каталог товаров, систему отзывов и защищенную административную панель для управления контентом.

## 🛠 Технологический стек

### Backend

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-0.0.16+-DE1F26?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLAdmin](https://img.shields.io/badge/SQLAdmin-0.16+-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Passlib](https://img.shields.io/badge/Passlib-bcrypt-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-3.1+-B41717?style=for-the-badge&logo=jinja&logoColor=white)

- **FastAPI** — современный async веб-фреймворк
- **SQLModel** — ORM для работы с БД (поддержка любых реляционных СУБД)
- **SQLAdmin** — административная панель
- **Pydantic** — валидация данных
- **PyJWT** — аутентификация через JWT-токены
- **Passlib** — хеширование паролей
- **Fastapi-storage** — управление загрузкой файлов
- **Jinja2** — шаблонизация HTML

### Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)

- **HTML/CSS/JavaScript** (Vanilla JS)
- **Figma** — разработка дизайн-макета
- Адаптивная верстка

### Database

![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Ready-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

- **SQLite** (в разработке) — легко заменяется на PostgreSQL/MySQL благодаря SQLModel

### Tools & Environment
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![Python-dotenv](https://img.shields.io/badge/.env-Config-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black)

## ✨ Функциональность

### Публичная часть
- 📄 **Одностраничный сайт** с разделами: О нас, Хиты продаж, Наше производство, Отзывы, Контакты
- 🛍️ **Динамический каталог товаров** — загрузка через API (`/api/product/`)
- 💬 **Система отзывов** — пользователи могут оставлять отзывы через форму
- 📱 **Responsive дизайн** с фирменным оранжевым цветом

### Административная панель
- 🔐 **JWT-аутентификация** с хешированием паролей
- ➕ **CRUD операции** для товаров, категорий и отзывов
- 📤 **Загрузка изображений** товаров через fastapi-storage
- 🎨 Интеграция через SQLAdmin

## 🗂 Структура проекта
```
XBOCTUK/
├── admin/              # Административная панель
│   ├── auth.py        # Настройка аутентификации SQLAdmin
│   └── views.py       # View-классы для моделей
├── core/              # Ядро приложения
│   ├── config.py      # Конфигурация из .env
│   └── security.py    # JWT и хеширование паролей
├── routers/           # API эндпоинты
│   ├── category.py    # GET /api/category/
│   ├── product.py     # GET /api/product/
│   ├── review.py      # GET, POST /api/review/
│   └── user.py        # POST /api/users/login/, GET /api/users/me/
├── static/            # Статические файлы
│   ├── images/        # Изображения (товары и контент)
│   ├── script.js      # Frontend логика
│   └── style.css      # Стили
├── templates/
│   └── index.html     # Основной шаблон (Jinja2)
├── database.py        # Подключение к БД
├── main.py            # Точка входа FastAPI
├── seed.py            # Заполнение БД демо-данными
└── requirements.txt
```

## 🗄 Модели данных

### Product (Товар)
```python
- id: int
- price: Decimal
- description: str
- brand: str | None
- country: str | None
- material: str | None
- animal_age: str | None
- image: FileType
- category_id: int (FK)
- is_hit: bool  # Отображение в "Хитах продаж"
```

### Category (Категория)
```python
- id: int
- title: str
- text: str
- products: Relationship
```

### Review (Отзыв)
```python
- id: int
- username: str
- email: str
- text: str
```

### User (Администратор)
```python
- id: int
- username: str
- hashed_password: str
- is_admin: bool
```

## 🚀 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/product/` | Получить все товары |
| GET | `/api/category/` | Получить все категории |
| GET | `/api/review/` | Получить все отзывы |
| POST | `/api/review/` | Создать новый отзыв |
| POST | `/api/users/login/` | Авторизация (JWT) |
| GET | `/api/users/me/` | Получить данные текущего пользователя |

> **Примечание:** API спроектирован с возможностью расширения до полноценного REST сервиса

## 🔐 Безопасность

- **JWT-токены** для аутентификации администраторов
- **Хеширование паролей** через bcrypt (passlib)
- **Переменные окружения** (.env) для чувствительных данных:

## 📦 Установка и запуск

1. **Клонировать репозиторий**
```bash
   git clone https://github.com/kuramagod/XBOCTUK.git
   cd XBOCTUK
```

2. **Создать виртуальное окружение**
```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
```

3. **Установить зависимости**
```bash
   pip install -r requirements.txt
```

4. **Настроить .env файл**
```bash
   cp .env.example .env
   # Заполнить переменные окружения
```

5. **Запустить сервер**
```bash
   uvicorn main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

Административная панель: `http://localhost:8000/admin`

API документация (Swagger): `http://localhost:8000/docs`

## 🎨 Дизайн

### Сайт

![Главная страница](screenshots/herosection.png)

### Админ панель

![Админ-панель](screenshots/adminpanel.png)

### Документация Swagger UI

![Swagger UI](screenshots/docs.png)

[Макет в Figma](https://www.figma.com/design/r1lidM8Qpm4KNJwBgNdLLI/csite?node-id=55-54&p=f&t=osOdHwBi8FuDXtkZ-0)

## 🏗 Архитектурные решения

- **Разделение на слои:** роутеры, модели, core-логика
- **SQLModel:** единая декларация Pydantic-схем и SQLAlchemy-моделей
- **Гибкость БД:** легкая замена SQLite на PostgreSQL/MySQL без изменения кода
- **Расширяемость:** структура проекта позволяет добавить полный CRUD API с минимальными изменениями
- **Jinja2 + Fetch API:** гибридный подход для рендеринга (статика + динамика)

## 📝 Возможности для расширения

- [ ] Полноценный CRUD API для всех сущностей
- [ ] Система ролей пользователей (покупатели/администраторы)
- [ ] Корзина и оформление заказов
- [ ] Пагинация и фильтрация товаров
- [ ] Интеграция платежных систем
- [ ] Миграции БД (Alembic)

## 📄 Лицензия

Учебный проект
