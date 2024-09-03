from dataclasses import dataclass
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base


class Metrics(Base):
    
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    archive = Column(String)
    logfile = Column(String)
    total = Column(Integer)
    parsed = Column(Integer)
    failed = Column(Integer)
    skipped = Column(Integer)


@dataclass
class MetricsStruct:
    archive: str
    logfile: str
    total: int = 0
    parsed: int = 0
    failed: int = 0
    skipped: int = 0