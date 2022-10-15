from sqlalchemy import Column, String, Integer, DateTime
from .Base import Base


class LoadedDay(Base):
    __tablename__ = "LoadedDays"

    id = Column(Integer, primary_key=True)
    file_date = Column(DateTime)
    fetch_date = Column(DateTime)
    train_date = Column(DateTime)
