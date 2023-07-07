from datetime import datetime

from sqlalchemy import Integer, String, Column, LargeBinary, \
    ForeignKey, Boolean, Double, TIMESTAMP

from src.config import SECRET_KEY
from src.database import Base
import bcrypt
import jwt


class ProductOrder(Base):
    """Models a ProductOrder table"""
    __tablename__ = "productOrders"
    id = Column(Integer, nullable=False, primary_key=True)
    id_product = Column(Integer, ForeignKey("products.id"))
    id_order = Column(Integer, ForeignKey("orders.id"))
    count = Column(Integer)


class IngredientsProduct(Base):
    """Models a IngredientsProduct table"""
    __tablename__ = "ingredientProducts"
    id = Column(Integer, nullable=False, primary_key=True)
    id_product = Column(Integer, ForeignKey("products.id"))
    id_ingredient = Column(Integer, ForeignKey("ingredients.id"))


class Ingredients(Base):
    """Models a ingredient table"""
    __tablename__ = "ingredients"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    count = Column(Double)


class Product(Base):
    """Models a product table"""
    __tablename__ = "products"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    availability = Column(Boolean)
    description = Column(String)


class Order(Base):
    """Models a order table"""
    __tablename__ = "orders"
    id = Column(Integer, nullable=False, primary_key=True)
    status = Column(String)
    id_user = Column(Integer, ForeignKey("users.id"))
    delivery = Column(Boolean)
    address = Column(String)
    id_chef = Column(Integer, ForeignKey("chefs.id"))
    id_couriers = Column(Integer, ForeignKey("couriers.id"))
    order_time = Column(TIMESTAMP, default=datetime.utcnow)
    cost = Column(Double)


class Promotion(Base):
    """Models a promotion table"""
    __tablename__ = "promotions"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)


class Courier(Base):
    """Models a courier table"""
    __tablename__ = "couriers"
    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    salary = Column(Double)


class Chef(Base):
    """Models a chef table"""
    __tablename__ = "chefs"
    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    salary = Column(Double)


class User(Base):
    """Models a user table"""
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    middle_surname = Column(String)
    phone = Column(String, nullable=False, unique=True)
    email = Column(String)
    hashed_password = Column(LargeBinary, nullable=False)
    address = Column(String)
    bonus = Column(Integer)
    role = Column(String)

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

    def generate_token(self) -> dict:
        """Generate access token for user"""
        return {
            "access_token": str(jwt.encode(
                {"name": self.first_name, "phone": self.phone, "id": self.id},
                SECRET_KEY
            ))
        }
