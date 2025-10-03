from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text
from database import Base
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(30), unique=True)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"User({self.username})"


class Order(Base):
    ORDER_STATUSES = [
        ("PENDING", "pending"),
        ("IN-TRANSIT", "in-transit"),
        ("DELIVERED", "delivered"),
    ]

    PIZZA_SIZES = [("SMALL", "small"), ("MEDIUM", "medium"), ("LARGE", "large")]

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, index=True)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES), default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), default="SMALL")
    user_id = Column(Integer, ForeignKey("customers.id"), index=True)
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"Order({self.id})"
