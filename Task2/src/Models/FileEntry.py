from sqlalchemy import Column, String, Integer, DateTime
from .Base import Base


class Entry(Base):
    __tablename__ = "Entries"

    id = Column(Integer, primary_key=True)
    client_user_id = Column(String)
    session_id = Column(String)
    dropped_frames = Column(Integer)
    FPS = Column(Integer)
    bitrate = Column(Integer)
    RTT = Column(Integer)
    timestamp = Column(DateTime)
    device = Column(String)
