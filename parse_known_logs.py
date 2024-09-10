import os
import logging
import io
import random
from tqdm import tqdm
from itertools import groupby
from operator import itemgetter

from sqlalchemy.orm import Session
from logtools.models import *
from logtools.parsers import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logging.basicConfig(level=logging.CRITICAL, format='[%(asctime)s] - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)


def parse_one_filetype(parser, directory, archive_filename, session: Session):
    stream = parser.parse_archive(directory, archive_filename)
    for model, records in groupby(stream, key=itemgetter(0)):
        records = (record for _, record in records)
        session.bulk_insert_mappings(model, records)
    session.commit()


def parse_into_db(directory, archive_filename, session):
    parsers = [
        # UplinkTxtParser(),
        # ManifestTxtParser(),
        # RuntimeTxtParser(),
        # CargoHtmlParser(),
        # SiloParser(),
        GameTxtParser(),
        # DynamicCombinedParser(),
    ]
    for parser in parsers:
        parse_one_filetype(parser, directory, archive_filename, session)


def parse_directory_into_db(directory, session, sample=None):
    files = os.listdir(directory)
    if sample:
        files = random.sample(files, sample)
    for archive_filename in tqdm(files):
        LOG.info("Parsing %s", archive_filename)
        parse_into_db(directory, archive_filename, session)


def main():
    random.seed(69)
    engine = create_engine("sqlite:///logs.sqlite")

    to_delete = [
        t for t in Base.metadata.tables.values() 
        if t.name not in ["round_archive_url"]
    ]
    Base.metadata.drop_all(engine, tables=to_delete)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    parse_directory_into_db("logs", session, sample=1000)


if __name__ == "__main__":
    main()