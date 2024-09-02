from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)

from .meta import Base


class GameSay(Base):

    __tablename__ = "game_say"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt = Column(DateTime)
    ckey = Column(String)
    mob_name = Column(String)
    mob_id = Column(String)
    reason = Column(String)
    text = Column(String)
    forced = Column(String)
    location = Column(String)
    ru = Column(Boolean)

    def __repr__(self) -> str:
        return f"<GameSay("\
                f"round_id={self.round_id!r}, "\
                f"dt={self.dt!r}, "\
                f"ckey={self.ckey!r}, "\
                f"mob_name={self.mob_name!r}, "\
                f"mob_id={self.mob_id!r}, "\
                f"reason={self.reason!r}, "\
                f"text={self.text!r}, "\
                f"forced={self.forced!r}, "\
                f"location={self.location!r}, "\
                f"ru={self.ru})>"