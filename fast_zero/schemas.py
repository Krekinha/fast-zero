from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    updated_at: datetime


class UserList(BaseModel):
    users: list[UserPublic]
