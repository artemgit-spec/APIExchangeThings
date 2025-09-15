from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated

from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.orm import Session

from schemes.schemes_thing import CreateThing, PrintThing, UpdateThing
from db.db_engine import session_db
from db.models import Thing
from core.security import oaut2, decode_token

router_thing = APIRouter(prefix="/things", tags=["Управление вещами"])


# эндпоинт для создания вещей
@router_thing.post("/create-thing")
async def create_thing(
    db: Annotated[Session, Depends(session_db)],
    token: Annotated[str, Depends(oaut2)],
    new_thing: CreateThing,
):
    info_user = decode_token(token)
    db.execute(
        insert(Thing).values(
            name=new_thing.name,
            description=new_thing.description,
            date_added=new_thing.date_added,
            user_id=info_user.get("id"),
        )
    )

    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "detail": "Создана карточка товара"}


# получение списка всех своих вещей
@router_thing.get("/my-things", response_model=list[PrintThing])
async def info_my_thing(
    db: Annotated[Session, Depends(session_db)], token: Annotated[str, Depends(oaut2)]
):
    info_user = decode_token(token)
    id = info_user.get("id")
    list_things = db.scalars(select(Thing).where(Thing.user_id == id)).all()
    return list_things


# получение списка всех вещей на площадке
@router_thing.get("/info-things")
async def all_my_things(
    db: Annotated[Session, Depends(session_db)], token: Annotated[str, Depends(oaut2)]
):
    my_things = db.scalars(select(Thing)).all()
    return my_things


# изменение информации о вещи
@router_thing.patch("/update-thing/{id}")
async def update_my_thing(
    db: Annotated[Session, Depends(session_db)],
    token: Annotated[str, Depends(oaut2)],
    up_thing: UpdateThing,
    id: int,
):
    info_user = decode_token(token)
    my_thing = db.scalar(
        select(Thing).where(and_(Thing.id == id, Thing.user_id == info_user.get("id")))
    )
    if not my_thing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого предмета"
        )
    if up_thing.name == "string" and up_thing.description == "string":
        answer = "Изменения не были внесены"
    elif up_thing.name == "string":
        my_thing.description = up_thing.description
        answer = f"Изменили описание на {up_thing.description}"
    elif up_thing.description == "string":
        my_thing.name = up_thing.name
        answer = f"Изменили название на {up_thing.name}"

    else:
        my_thing.name = up_thing.name
        my_thing.description = up_thing.description
        answer = (
            f"Изменили название на {up_thing.name} и описание на {up_thing.description}"
        )
    db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": answer}


# эндпоинт для удаления вещей
@router_thing.delete("/delete-thing/{id}")
async def delete_my_thing(
    db: Annotated[Session, Depends(session_db)],
    token: Annotated[str, Depends(oaut2)],
    id: int,
):
    info_user = decode_token(token)
    my_thing = db.scalar(
        select(Thing).where(and_(Thing.id == id, Thing.user_id == info_user.get("id")))
    )
    if not my_thing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет такого предмета"
        )
    db.execute(delete(Thing).where(Thing.id == id))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": "Предмет удален"}
