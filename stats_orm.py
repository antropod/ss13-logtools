import pandas as pd
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker

from logtools.models.uplink import Uplink


# select
#    item,
#    count(*) as rounds,
#    sum(purchases) as purchases
# from (
#     select
#         round_id,
#         item,
#         count(*) as purchases
#     from uplink
#     group by
#         round_id, item
# )
# group by item
# order by rounds desc;

def run_query(session):
    inner = session\
        .query(
            Uplink.round_id,
            Uplink.item,
            func.count().label('purchases'),
        )\
        .group_by(Uplink.round_id, Uplink.item)\
        .subquery(name="t")
    outer = session\
        .query(
            inner.c.item.label("item"),
            func.sum(inner.c.purchases).label("purchases"),
            func.count().label('rounds')
        )\
        .group_by("item")\
        .order_by(desc("purchases"))
    for q in outer:
        print(q)



def main():
    engine = create_engine("sqlite:///logs.db")
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        run_query(session)


if __name__ == "__main__":
    main()