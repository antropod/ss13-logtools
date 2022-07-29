from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from .meta import Base


class Uplink(Base):
    __tablename__ = "uplink"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt = Column(DateTime)
    ckey = Column(String)
    name = Column(String)
    item = Column(String)
    discount = Column(Integer)
    price = Column(Integer)

    def __repr__(self) -> str:
        return f"<Uplink("\
                f"round_id={self.round_id!r}, "\
                f"dt={self.dt!r}, "\
                f"ckey={self.ckey!r}, "\
                f"name={self.name!r}, "\
                f"item={self.item!r}, "\
                f"discount={self.discount!r}, "\
                f"price={self.price!r})>"


class Changeling(Base):
    __tablename__ = "changeling"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt = Column(DateTime)
    ckey = Column(String)
    name = Column(String)
    power = Column(String)

    def __repr__(self) -> str:
        return f"<Changeling("\
                f"round_id={self.round_id!r}, "\
                f"dt={self.dt!r}, "\
                f"ckey={self.ckey!r}, "\
                f"name={self.name!r}, "\
                f"power={self.power!r})>"
