from sqlalchemy import select
from db.db_engine import session
from db.models import Admin, User
from core.security import get_hash_pass


async def init_info_db():
    db = session()
    try:
        if not db.scalar(select(Admin).filter(Admin.name == "admin1")):
            admin1 = Admin(
                name="admin1",
                password=get_hash_pass("admin1"),
                email="user@example.com",
            )
        if not db.scalar(select(User).filter(User.name == "user1")):
            user1 = User(
                name="user1",
                password=get_hash_pass("user1"),
                email="user@example.com",
            )
        db.add_all([admin1, user1])
        db.commit()
    finally:
        db.close()
