from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from .meta import Base


class Manifest(Base):

    __tablename__ = "manifest"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt = Column(DateTime)
    ckey = Column(String)
    name = Column(String)
    assigned_role = Column(String)
    special_role = Column(String)
    latejoin = Column(String)

    def __repr__(self) -> str:
        return f"<Manifest("\
                f"round_id={self.round_id!r}, "\
                f"dt={self.dt!r}, "\
                f"ckey={self.ckey!r}, "\
                f"name={self.name!r}, "\
                f"assigned_role={self.assigned_role!r}, "\
                f"special_role={self.special_role!r}, "\
                f"latejoin={self.latejoin!r})>"
