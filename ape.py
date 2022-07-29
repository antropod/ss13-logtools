import os
import logging
import io

from logtools.models.meta import Base
from logtools.models.uplink import Uplink
from logtools.parsers.uplink import UplinkTxtParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)




def parse_into_db(directory, archive_filename, session):
    parser = UplinkTxtParser()
    for record in parser.parse_file_from_archive(directory, archive_filename):
        session.add(record)
    session.commit()


def parse_directory_into_db(directory, session):
    session.query(Uplink).delete()
    session.commit()

    for archive_filename in os.listdir(directory):
        LOG.info("Parsing %s", archive_filename)
        parse_into_db(directory, archive_filename, session)


def main():
    engine = create_engine("sqlite:///logs.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    parse_directory_into_db("logs_2022", session)


if __name__ == "__main__":
    main()