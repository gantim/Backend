from typing import Dict, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.config import SECRET_KEY
from src.models import models as user_model

from src.database import get_db
from src.models.models import User
from src.schemas.user import UserSchema, CreateUserSchema, UserOutSchema
from src.services.db import user as user_db_services
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

@router.post('/recovery')
def password_recovery(payload: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):

    user = user_db_services.get_user(session, payload.phone)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "Password recovery link sent"}

@router.post('/signup', response_model=UserSchema)
def signup(
        payload: CreateUserSchema = Body(),
        session: Session = Depends(get_db)
):
    """Processes request to register user account."""
    payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
    return user_db_services.create_user(session, user=payload)

@router.post('/login', response_model=Dict)
def login(payload: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_db)
          ):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email,
                phone number, name

    - password:
    """
    try:
        user: user_model.User = user_db_services.get_user(
            session=session, phone=payload.username
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    return user.generate_token()


@router.get("/current", response_model=UserOutSchema)
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(User).get(data["id"])
    return stmt