from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)

from .meta import Base


class Game(Base):
    
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    category = Column(String, nullable=False)
    dt = Column(DateTime)
    ckey = Column(String)
    mob_name = Column(String)
    mob_id = Column(String)
    reason = Column(String)
    text = Column(String)
    forced = Column(String)
    location = Column(String)
    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)
    ru = Column(Boolean)
