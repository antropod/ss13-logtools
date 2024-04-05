from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from .meta import Base


class CargoShippedOrder(Base):

    __tablename__ = "cargo_order"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt = Column(DateTime)
    order = Column(String)
    ordered_by = Column(String)
    paid_by = Column(String)
