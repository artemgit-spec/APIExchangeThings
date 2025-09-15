from pydantic import BaseModel
from datetime import datetime


class CreateThing(BaseModel):
    name: str
    description: str
    date_added: datetime = datetime.now()


class PrintThing(BaseModel):
    id: int
    name: str
    description: str
    date_added: datetime


class UpdateThing(BaseModel):
    name: str
    description: str
