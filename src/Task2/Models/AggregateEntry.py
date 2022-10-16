from sqlalchemy import Column, String, Integer, DateTime, Float
from .Base import Base


class AggregateEntry(Base):
    __tablename__ = "AggregateEntries"

    id = Column(Integer, primary_key=True)
    client_user_id = Column(String)
    session_id = Column(String)
    session_start = Column(DateTime)
    session_end = Column(DateTime)
    dropped_frames_min = Column(Float)
    dropped_frames_mean = Column(Float)
    FPS_min = Column(Float)
    FPS_max = Column(Float)
    FPS_mean = Column(Float)
    FPS_std = Column(Float)
    RTT_min = Column(Float)
    RTT_max = Column(Float)
    RTT_mean = Column(Float)
    RTT_std = Column(Float)
    bitrate_min = Column(Float)
    bitrate_max = Column(Float)
    bitrate_mean = Column(Float)
    bitrate_std = Column(Float)
    device = Column(String)
    duration = Column(Float)
