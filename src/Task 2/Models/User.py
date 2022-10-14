from sqlalchemy import Column, String, Integer
from .Base import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    client_user_id = Column(String, unique=True)
