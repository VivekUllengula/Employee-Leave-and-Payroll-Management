from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.mongo import get_db
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_user_by_email(db, email: str):
    return await db.users.find_one({"email": email})

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: dict, expires_minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.JWT_ACCESS_TOKEN_EXPIRES_MIN)
    to_encode = {"exp": expire, **subject}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    from jose import JWTError
    from app.models.user import TokenPayload
    db = get_db()
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},  # adjust if you use audience
        )
        # Validate with your Pydantic model if available
        token_data = TokenPayload(**payload) if TokenPayload else payload  # type: ignore
    except JWTError:
        raise credentials_exception
    except Exception:
        # Covers pydantic validation errors or other issues
        raise credentials_exception
 
    # Extract an email-like identifier
    email = (
        getattr(token_data, "email", None)
        or getattr(token_data, "sub", None)
        or payload.get("email")
        or payload.get("sub")
    )
    if not email:
        raise credentials_exception
 
    user = await get_user_by_email(db, email)
    if not user:
        raise credentials_exception
 
    return user
    