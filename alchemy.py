import sqlite3

from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Sequence,
    ForeignKey,
    MetaData,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class UplinkLog(Base):
    __tablename__ = "uplink_log"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt = Column(DateTime)
    logtype = Column(String)
    ckey = Column(String)
    name = Column(String)
    item = Column(String)
    discount = Column(Integer)
    price = Column(Integer)
    source = Column(String)

    def __repr__(self) -> str:
        return f"<UplinkLog("\
                f"round_id={self.round_id!r}, "\
                f"dt={self.dt!r}, "\
                f"logtype={self.logtype!r}, "\
                f"ckey={self.ckey!r}, "\
                f"name={self.name!r}, "\
                f"item={self.item!r}, "\
                f"discount={self.discount!r}, "\
                f"price={self.price!r}, "\
                f"source={self.source!r})>"\


def create_models(engine):
    Base.metadata.create_all(engine)
