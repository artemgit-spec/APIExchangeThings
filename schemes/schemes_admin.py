from pydantic import BaseModel, EmailStr


class CreateAdmin(BaseModel):
    name: str = "admin"
    password: str = "admin"
    email: EmailStr


class InfoUser(BaseModel):
    name: str
