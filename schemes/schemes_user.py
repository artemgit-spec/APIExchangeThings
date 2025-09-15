from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    name: str = "user"
    password: str = "user"
    email: EmailStr


class UpdateUser(BaseModel):
    name: str = None
    email: str = None


class InfoUser(BaseModel):
    id: int
    name: str
    email: str
