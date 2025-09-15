# APIExchangeThings
Приложение для бартерного обмена вещами
Стек технологий:

- [FastAPI](https://fastapi.tiangolo.com/) — backend-фреймворк
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [PostgreSQL](https://www.postgresql.org/) — база данных
- [Alembic](https://alembic.sqlalchemy.org/) — миграции
- [Pytest](https://docs.pytest.org/) — тестирование
- [JWT](https://jwt.io/) — авторизация
- [Pydantic](https://docs.pydantic.dev/) — валидация данных

Структура проекта:
APIExchangeThings/
├── core/               # Создание токена
├── db/                 # БД и SQLAlchemy модели
├── migration/          # Миграции
├── routers/            # FastAPI маршруты
├── schemas/            # Pydantic-схемы
├── test/              # Тесты
├── alembic.ini
├── main.py             # Точка входа
├── pytest.ini
├── README.md
└── requirements.txt

Запуск сервера: 
uvicorn main:app --reload

Запуск тестов:
pytest