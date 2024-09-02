import os
import random
from common import Session
import logging
import datetime

from logtools.models import *
from logtools.parsers import *


logging.basicConfig(level=logging.ERROR, format='%(message)s')
LOG = logging.getLogger(__name__)


def get_random_sample(directory, sample=1):
    files = os.listdir(directory)
    return random.sample(files, k=sample)


def get_sample_logs(directory):
    files = os.listdir(directory)[:100]
    return files


def main():
    parser = GameTxtParser()
    for filename in get_random_sample("logs", 100):
        records = parser.parse_file_from_archive("logs", filename)
        for r in records:
            pass


if __name__ == "__main__":
    main()