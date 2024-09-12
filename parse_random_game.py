import os
import random
from common import Session, engine, SQL_DIR
import logging
import datetime

from logtools.util import read_file
from logtools.models import *
from logtools.parsers import *
from sqlalchemy import text


logging.basicConfig(level=logging.WARNING, format='%(message)s')
LOG = logging.getLogger(__name__)


def get_random_sample(directory, sample=1):
    files = os.listdir(directory)
    return random.sample(files, k=sample)


def get_sample_logs(directory):
    files = os.listdir(directory)[:100]
    return files


def get_rounds_from_sql(sql_filename):
    query = read_file(os.path.join(SQL_DIR, sql_filename))
    with engine.connect() as conn:
        result = conn.execute(text(query))
        for r in result:
            yield r[0]


def main():
    parser = GameTxtParser()
    for filename in ["round-209595.zip"]:
    # for filename in get_random_sample("logs", 100):
        records = parser.parse_archive("logs", filename)
        for r in records:
            pass


if __name__ == "__main__":
    main()