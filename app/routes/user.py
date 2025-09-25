from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserInDB, Token
from app.services.user_service import UserService
from app.db.mongo import get_db
from app.utils.auth import get_current_user
from app.utils.mongo_helpers import convert_mongo_document
 
router = APIRouter(prefix="/auth", tags=["Authentication"])
 
@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate, db=Depends(get_db)):
    """Register a new user"""
    service = UserService(db)
    new_user = await service.create_user(user)
    return UserInDB(**convert_mongo_document(new_user))
 
 
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)
):
    """Login and return JWT token"""
    service = UserService(db)
    user = await service.authenticate_user(form_data.username, form_data.password)
    return convert_mongo_document(service.create_token(user)) 
 
@router.post("/logout")
async def logout(request: Request, db=Depends(get_db)):
    service = UserService(db)
    token = request.headers.get("Authorization")
    return await service.logout_user(token)

@router.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    """Get details of the current logged-in user"""
    return convert_mongo_document(current_user)