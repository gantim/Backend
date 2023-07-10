from sqlalchemy.orm import Session

from src.models.models import Address
from src.schemas.address import AddressBaseSchema


def create_address(session: Session, address: AddressBaseSchema):
    db_address = Address(**address.dict())
    session.add(db_address)
    session.commit()
    session.refresh(db_address)
    return db_address
