import uplink
import alchemy
from alchemy import UplinkLog

from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import sessionmaker
import os

import logging


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)


def parse_into_db(directory, archive_filename, session):
    for record in uplink.parse_from_archive(directory, archive_filename, "uplink.txt"):
        round_id, dt, type_, ckey, name, item, discount, price, source = record
        record = UplinkLog(
            round_id=round_id,
            dt=dt,
            logtype=type_,
            ckey=ckey,
            name=name,
            item=item,
            discount=discount,
            price=price,
            source=source,
        )
        session.add(record)
    session.commit()


def parse_directory_into_db(directory, session):
    session.query(UplinkLog).delete()
    session.commit()

    for archive_filename in os.listdir(directory):
        LOG.info("Parsing %s", archive_filename)
        parse_into_db(directory, archive_filename, session)


def main():
    engine = create_engine("sqlite:///logs.db")
    alchemy.create_models(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    parse_directory_into_db("logs_2022", session)


if __name__ == "__main__":
    main()