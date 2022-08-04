from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
)

from .meta import Base


class RoundArchiveUrl(Base):

    __tablename__ = "round_archive_url"

    round_id = Column(Integer, primary_key=True)
    server = Column(String)
    dt = Column(Date)
    url = Column(String)