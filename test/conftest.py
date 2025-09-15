import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.db_engine import session_db
from db.models import Base, Admin, User, Thing, Deal
from core.security import get_hash_pass

TEST_BASE = "sqlite:///test.db"


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(TEST_BASE, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_session(test_db):
    test_session = sessionmaker(bind=test_db)
    session = test_session()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    admin = Admin(
        name="admin",
        password=get_hash_pass("admin"),
        email="user@example.com",
    )

    user1 = User(
        name="user1",
        password=get_hash_pass("user1"),
        email="user@example.com",
    )
    user2 = User(
        name="user2",
        password=get_hash_pass("user2"),
        email="user@example.com",
    )
    user3 = User(
        name="user3",
        password=get_hash_pass("user3"),
        email="user@example.com",
    )
    user4 = User(
        name="user4",
        password=get_hash_pass("user4"),
        email="user@example.com",
    )
    session.add_all([admin, user1, user2, user3, user4])
    session.commit()
    thing1 = Thing(
        name="ноутбук",
        description="string",
        date_added=datetime.now(),
        user_id=user1.id,
    )
    thing2 = Thing(
        name="телефон",
        description="string",
        date_added=datetime.now(),
        user_id=user1.id,
    )
    thing3 = Thing(
        name="часы", description="string", date_added=datetime.now(), user_id=user2.id
    )
    thing4 = Thing(
        name="наушники",
        description="string",
        date_added=datetime.now(),
        user_id=user2.id,
    )
    thing5 = Thing(
        name="колонка",
        description="string",
        date_added=datetime.now(),
        user_id=user3.id,
    )

    session.add_all([thing1, thing2, thing3, thing4, thing5])
    session.commit()
    deal1 = Deal(
        id_my_thing=thing2.id,
        id_thing_exchange=thing4.id,
        answer_user=None,
        begin_exchange=datetime.fromisoformat("2025-09-09T08:57:55.478953"),
        sender_id=user1.id,
        receiver_id=user2.id,
    )
    deal2 = Deal(
        id_my_thing=thing1.id,
        id_thing_exchange=thing3.id,
        answer_user=None,
        begin_exchange=datetime.fromisoformat("2025-09-09T08:57:55.478953"),
        sender_id=user1.id,
        receiver_id=user2.id,
    )
    session.add_all([deal1, deal2])
    session.commit()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def client(test_session):
    def override_get_db():
        try:
            yield test_session
        finally:
            test_session.close()

    app.dependency_overrides[session_db] = override_get_db
    return TestClient(app)


users = {
    "admin": {"username": "admin", "password": "admin"},
    "user1": {"username": "user1", "password": "user1"},
    "user2": {"username": "user2", "password": "user2"},
    "user3": {"username": "user3", "password": "user3"},
    "user4": {"username": "user4", "password": "user4"},
}


@pytest.fixture
def token(client, request):
    creds = users[request.param]
    response = client.post(f"/token", data=creds)
    assert response.status_code == 200
    token = response.json().get("access_token")
    return f"Bearer {token}"
