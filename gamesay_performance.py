import os
import logging
import io
from tqdm import tqdm

from logtools.models import *
from logtools.parsers.manifest import ManifestTxtParser
from logtools.parsers.uplink import UplinkTxtParser
from logtools.parsers.game import GameTxtParser
from logtools.parsers.runtime import RuntimeTxtParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logging.basicConfig(level=logging.CRITICAL, format='[%(asctime)s] - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)


def parse_directory_into_db(directory, session):
    to_delete = [Uplink, Changeling, Manifest, GameSay, MapInfo]
    for model in to_delete:
        session.query(model).delete()
    session.commit()

    parser = GameTxtParser()
    for archive_filename in tqdm(os.listdir(directory)):
        for record in parser.parse_file_from_archive(directory, archive_filename):
            session.add(record)
    session.commit()


def main():
    engine = create_engine("sqlite:///logs.sqlite")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    parse_directory_into_db("logs", session)


if __name__ == "__main__":
    main()