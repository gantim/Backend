from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.models.models import User
from src.schemas.user import CreateUserSchema
import requests


def create_user(session: Session, user: CreateUserSchema):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(session: Session, phone: str):
    return session.query(User).filter(User.phone == phone).one()

def send_password_reset_link(phone: str, reset_link: str):
    api_key = "57955791-B97D-8754-D86A-286BDC198C65"
    sms_ru_api_url = "https://sms.ru/sms/send"

    params = {
    "api_id": api_key,
    "to": phone,
    "msg": f"Hello,\n\nYou have requested to reset your password. Please click the link below:\n\n{reset_link}",
    "json": 1
    }

    response = requests.post(sms_ru_api_url, data=params)

    if response.status_code == 100:
        data = response.json()
        if data["status"] == "OK":
            print("Password recovery SMS sent")
        else:
            print("Failed to send password recovery SMS")
    else:
        print("Failed to send password recovery SMS")