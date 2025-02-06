from pydantic import BaseModel, EmailStr
from typing import Union

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[EmailStr, None] = None

class UserRequest(User):
    password: str

class UserInDB(User):
    hashed_password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None