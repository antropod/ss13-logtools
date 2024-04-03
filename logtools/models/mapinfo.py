from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from .meta import Base


class MapInfo(Base):

    __tablename__ = "mapinfo"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt = Column(DateTime)
    map_name = Column(String)