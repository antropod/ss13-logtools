from dataclasses import dataclass, astuple
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
)

from .meta import Base


#"threat_level":42,"round_start_budget":32.3,"mid_round_budget":9.7,"shown_threat":43
class Dynamic(Base):
    
    __tablename__ = "dynamic"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt_start = Column(DateTime)
    threat_level = Column(Float)
    round_start_budget = Column(Float)
    mid_round_budget = Column(Float)
    shown_threat = Column(Float)
    players_ready = Column(Integer)


@dataclass
class DynamicStruct:
    round_id: int
    dt_start: datetime
    threat_level: float = None
    round_start_budget: float = None
    mid_round_budget: float = None
    shown_threat: float = None
    players_ready: int = None

    def is_filled(self):
        return all(x is not None for x in astuple(self))
