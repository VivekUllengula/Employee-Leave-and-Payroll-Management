from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.mongo import get_db
from app.models.user import TokenPayload
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
 
async def get_user_by_email(db, email: str):
    return await db.users.find_one({"email": email})
 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
 
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
 
def create_access_token(
    subject: str, role: str, expires_minutes: int | None = None
) -> str:
    """Generate JWT token"""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.JWT_ACCESS_TOKEN_EXPIRES_MIN
    )
    to_encode = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
 
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db=Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},  # skip audience check
        )
        token_data = TokenPayload(**payload)
    except (JWTError, Exception):
        raise credentials_exception
    
    # extract identifier
    user_id_or_email = token_data.sub
    if not user_id_or_email:
        raise credentials_exception
    user = await get_user_by_email(db, user_id_or_email)
    if not user:
        raise credentials_exception
    return user

 