from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated
from enum import Enum
from datetime import datetime

from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session

from schemes.schemes_deal import CreateDeal, InfoDeal
from db.db_engine import session_db
from db.models import Deal, Thing
from core.security import oaut2, decode_token


router_deal = APIRouter(prefix="/deals", tags=["Управление сделками"])


# создание сделки
@router_deal.post("/create-deal")
async def create(
    db: Annotated[Session, Depends(session_db)],
    token: Annotated[str, Depends(oaut2)],
    new_deal: CreateDeal,
):
    info_user = decode_token(token)
    thing = db.scalar(select(Thing).where(Thing.id == new_deal.exchange_thing_id))
    if not thing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет такой вещи"
        )

    db.execute(
        insert(Deal).values(
            id_my_thing=new_deal.my_thing_id,
            id_thing_exchange=new_deal.exchange_thing_id,
            answer_user=None,
            begin_exchange=datetime.now(),
            sender_id=info_user.get("id"),
            receiver_id=thing.user_id,
        )
    )

    db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": "Сделка отправлена"}


# добавить сортировку сделок по статусу ответа.
@router_deal.get("/my-deals", response_model=list[InfoDeal])
async def all_my_deal(
    db: Annotated[Session, Depends(session_db)], token: Annotated[str, Depends(oaut2)]
):
    info_user = decode_token(token)
    id = info_user.get("id")
    my_deals = db.scalars(select(Deal).where(Deal.sender_id == id)).all()
    return my_deals


# выводит список все направленных пользователю сделок
@router_deal.get("/deals-exchange", response_model=list[InfoDeal])
async def exhange_deals(
    db: Annotated[Session, Depends(session_db)], token: Annotated[str, Depends(oaut2)]
):
    info_user = decode_token(token)
    my_deals_exchange = db.scalars(
        select(Deal).where(Deal.receiver_id == info_user.get("id"))
    ).all()
    return my_deals_exchange


class Decision(str, Enum):
    approved: str = "одобрить"
    rejected: str = "отклонить"


# эндпоинт для одобрения сделок
@router_deal.patch("/decision-deal/{id}")
async def dec_deal(
    db: Annotated[Session, Depends(session_db)],
    token: Annotated[str, Depends(oaut2)],
    dec: Decision,
    id: int,
):

    if dec == "одобрить":
        db.execute(
            update(Deal)
            .where(Deal.id == id)
            .values(answer_user=True, end_exchange=datetime.now())
        )
        db.execute(
            update(Thing)
            .where(Thing.id == Deal.id_my_thing)
            .values(
                user_id=Deal.receiver_id,
            )
        )
        db.execute(
            update(Thing)
            .where(Thing.id == Deal.id_thing_exchange)
            .values(user_id=Deal.sender_id)
        )
        db.commit()
        return {"status_code": status.HTTP_200_OK, "detail": "Сделка одобрена"}

    elif dec == "отклонить":
        db.execute(
            update(Deal)
            .where(Deal.id == id)
            .values(answer_user=False, end_exchange=datetime.now())
        )
        db.commit()
        return {"status_code": status.HTTP_200_OK, "detail": "Сделка отклонена"}
