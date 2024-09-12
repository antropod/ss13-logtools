from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
)

from .meta import Base


class RoundEndData(Base):
    
    __tablename__ = "round_end_data"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    nukeop_result=Column(String)
    station_integrity=Column(Float)
    station_destroyed=Column(Boolean)

