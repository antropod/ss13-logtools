from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from .meta import Base


# don't forget to change the Silo model if you are changing this
KNOWN_MATERIALS = [
    "iron",
    "glass",
    "plasma",
    "gold",
    "silver",
    "titanium",
    "uranium"
    "bluespace_crystal",
    "diamond",
    "plastic",
    "bananium",
]

class Silo(Base):

    __tablename__ = "silo"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer)
    dt = Column(DateTime)
    machine = Column(String)
    loc = Column(String)
    action = Column(String)
    amount = Column(Integer)
    item = Column(String)

    iron = Column(Integer, default=0)
    glass = Column(Integer, default=0)
    plasma = Column(Integer, default=0)
    gold = Column(Integer, default=0)
    silver = Column(Integer, default=0)
    titanium = Column(Integer, default=0)
    uranium = Column(Integer, default=0)
    bluespace_crystal = Column(Integer, default=0)
    diamond = Column(Integer, default=0)
    plastic = Column(Integer, default=0)
    bananium = Column(Integer, default=0)
    
    def materials(self):
        result = {}
        for m in KNOWN_MATERIALS:
            value = getattr(self, m)
            if value:
                result[m] = value
        return result

    def __repr__(self) -> str:
        return f"Silo("\
                f"round_id={self.round_id!r}, "\
                f"dt={self.dt!r}, "\
                f"machine={self.machine!r}, "\
                f"loc={self.loc!r}, "\
                f"action={self.action!r}, "\
                f"amount={self.amount!r}, "\
                f"item={self.item!r}, "\
                f"machine={self.machine!r}, "\
                f"materials={self.materials()!r})"
