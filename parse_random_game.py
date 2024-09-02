import os
import random
from common import Session
import logging
import datetime

from logtools.models import *
from logtools.parsers import *


logging.basicConfig(level=logging.CRITICAL, format='%(message)s')
LOG = logging.getLogger(__name__)


def get_random_sample(directory, sample=1):
    files = os.listdir(directory)
    return random.sample(files, k=sample)


def get_sample_logs(directory):
    files = os.listdir(directory)[:100]
    return files


def main():
    materials = set()
    parser = GameTxtParser()
    #for filename in get_random_sample("logs", 100):
    for filename in ["round-221496.zip"]:
        records = parser.parse_file_from_archive("logs", filename)
        for r in records:
            if r[1]["ckey"] == 'Kawaiinick' and r[1]["dt"] == datetime.datetime(2024, 1, 1, 18, 56, 15, 615):
                print(r)


if __name__ == "__main__":
    main()