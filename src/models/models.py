from sqlalchemy import MetaData, Integer, String, Column, LargeBinary, ForeignKey, Boolean, Table
from src.database import Base
import bcrypt

# metadata = MetaData()
#
# user = Table(
#     "user",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String)
# )


class User(Base):
    """Models a user table"""
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    phone = Column(String, nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    city = Column(String)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    photo_user = Column(String)

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {phone!r}>".format(phone=self.phone)

    @staticmethod
    def hash_password(password) -> bytes:
        """Transforms password from it's raw textual form to
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool:
        """Confirms password validity"""
        return bcrypt.checkpw(password.encode(), self.hashed_password)
