from pydantic import BaseModel, Field, EmailStr
from app.models.common import DBModelMixin

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str
    role: str = Field(default="admin", pattern=r"^(admin|hr|manager)$")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(DBModelMixin):
    email: EmailStr
    hashed_password: str
    full_name: str
    role: str = "admin"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: int
 