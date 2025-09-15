from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class CreateDeal(BaseModel):
    my_thing_id: int
    exchange_thing_id: int


class InfoDeal(BaseModel):
    id_my_thing: int
    id_thing_exchange: int
    answer_user: Optional[str] = None
    begin_exchange: datetime
    model_config = ConfigDict(from_attributes=True)
