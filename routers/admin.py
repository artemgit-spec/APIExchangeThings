from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated
from enum import Enum

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from db.db_engine import session_db
from db.models import Admin, User
from schemes.schemes_admin import CreateAdmin, InfoUser
from core.security import oaut2, get_hash_pass, decode_token

router_admin = APIRouter(prefix="/admin", tags=["Кабинет администратора"])


# регистрация нового администратора
@router_admin.post("/reg-admin")
async def create_admin(
    db: Annotated[Session, Depends(session_db)], create: CreateAdmin
):
    db.execute(
        insert(Admin).values(
            name=create.name,
            password=get_hash_pass(create.password),
            email=create.email,
        )
    )
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "default": "Создан новый администратор",
    }


class FilterUser(str, Enum):
    admin: str = "admins"
    user: str = "users"


# получение списков зарегистрированных пользователей.
@router_admin.get("/all-admins", response_model=list[InfoUser])
async def all_list_admins(
    db: Annotated[Session, Depends(session_db)],
    token: Annotated[str, Depends(oaut2)],
    filter: FilterUser,
):
    info_admin = decode_token(token)
    access_admin = db.scalar(select(Admin).where(Admin.id == info_admin.get("id")))
    if access_admin:
        if filter == "admins":
            list_admins = db.scalars(select(Admin)).all()
            return list_admins
        else:
            list_users = db.scalars(select(User)).all()
            return list_users
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="У вас недостаточно прав"
        )
