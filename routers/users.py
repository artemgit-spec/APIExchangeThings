from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated

from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

from schemes.schemes_user import CreateUser, UpdateUser, InfoUser
from db.db_engine import session_db
from db.models import User
from core.security import oaut2, get_hash_pass, decode_token

router_user = APIRouter(prefix="/user", tags=["Кабинет пользователя"])


# регистрация пользователя
@router_user.post("/reg-user")
async def create_user(db: Annotated[Session, Depends(session_db)], create: CreateUser):
    db.execute(
        insert(User).values(
            name=create.name,
            password=get_hash_pass(create.password),
            email=create.email,
        )
    )
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "detail": "Пользователь зарегистрирован",
    }


# проверка информации о себе
@router_user.get("/my_info", response_model=InfoUser)
async def info_users(
    db: Annotated[Session, Depends(session_db)], token: Annotated[str, Depends(oaut2)]
):
    info_user = decode_token(token)
    user = db.scalar(select(User).where(User.id == info_user.get("id")))
    return user


# изменение своей информации
@router_user.patch("/update-info")
async def update_info_user(
    db: Annotated[Session, Depends(session_db)],
    token: Annotated[Session, Depends(oaut2)],
    up_info: UpdateUser,
):
    info_user = decode_token(token)
    if up_info.name == "string" and up_info.email == "string":
        answer = "Изменения не были внесены"
    elif up_info.name == "string":
        db.execute(
            update(User)
            .where(User.id == info_user.get("id"))
            .values(email=up_info.email)
        )
        answer = f"Адрес почты изменили на {up_info.email}"
    elif up_info.email == "string":
        db.execute(
            update(User).where(User.id == info_user.get("id")).values(name=up_info.name)
        )
        answer = f"Логин изменили на {up_info.name}"
    else:
        answer = "Изменены логин и пароль"

    db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": answer}


# удаление своего профиля
@router_user.delete("/delete")
async def delete_user(
    db: Annotated[Session, Depends(session_db)], token: Annotated[str, Depends(oaut2)]
):
    info_user = decode_token(token)
    db.execute(delete(User).where(User.id == info_user.get("id")))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": "Вы удалили свой аккаунт"}
