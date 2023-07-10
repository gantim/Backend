from typing import Dict, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import update as sqlalchemy_update

from src.config import SECRET_KEY
from src.models import models as user_model

from src.database import get_db
from src.models.models import User, Address
from src.schemas.address import AddressSchema, AddressBaseSchema
from src.schemas.user import UserSchema, CreateUserSchema, UserOutSchema
from src.services.db import user as user_db_services
from src.services.db import address as address_db_services
import jwt

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


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


@router.post("/address", response_model=AddressSchema)
def add_address(token: Annotated[str, Depends(oauth2_scheme)],
                payload: AddressBaseSchema = Body(),
                session: Session = Depends(get_db)
                ):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    payload.id_user = data["id"]
    return address_db_services.create_address(session, address=payload)


@router.put("/address")
def edit_address(token: Annotated[str, Depends(oauth2_scheme)],
                 payload: AddressSchema = Body(),
                 session: Session = Depends(get_db)
                 ):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    payload.id_user = data["id"]
    stmt = sqlalchemy_update(Address).where(
        Address.id == payload.id).values(**payload.dict())
    session.execute(stmt)
    session.commit()
    return {'Status: 200 OK'}


@router.delete("/address")
def delete_address(id_address: int,
                   token: Annotated[str, Depends(oauth2_scheme)],
                   session: Session = Depends(get_db)
                   ):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    address = session.query(Address).filter_by(id=id_address).first()
    session.delete(address)
    session.commit()
    return {'Status: 200 OK'}
