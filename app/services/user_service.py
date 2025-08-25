from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.models.user import UserCreate
from fastapi import HTTPException, status
from datetime import timedelta
 
 
class UserService:
    def __init__(self, db):
        self.db = db
 
    async def get_user_by_email(self, email: str):
        return await self.db.users.find_one({"email": email})
 
    async def create_user(self, user: UserCreate):
        existing = await self.get_user_by_email(user.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
 
        hashed_pw = get_password_hash(user.password)
        user_dict = {
            "email": user.email,
            "hashed_password": hashed_pw,
            "full_name": user.full_name,
            "role": user.role,
        }
 
        result = await self.db.users.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        return user_dict
 
    async def authenticate_user(self, email: str, password: str):
        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
 
    def create_token(self, user: dict, expires_minutes: int = 30):
        token = create_access_token(
            subject=user["email"], role=user["role"], expires_minutes=expires_minutes
        )
        return {"access_token": token, "token_type": "bearer"}