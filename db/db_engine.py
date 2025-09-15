from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///things.db", echo=True)
session = sessionmaker(bind=engine)


async def session_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# "postgresql+psycopg2://exchangetable:exchange@localhost:5432/12345"
# "sqlite:///things.db"
