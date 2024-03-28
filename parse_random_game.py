import os
import random
from common import Session
import logging

from logtools.parsers.game import GameTxtParser
from logtools.models.manifest import Manifest

logging.basicConfig(level=logging.CRITICAL, format='%(message)s')
LOG = logging.getLogger(__name__)


def get_random_log(directory):
    files = os.listdir(directory)
    return random.choice(files)


def get_sample_logs(directory):
    files = os.listdir(directory)[:100]
    return files


def main():
    parser = GameTxtParser()
    for filename in get_sample_logs("logs"):
        records = parser.parse_file_from_archive("logs", filename)
        for r in records:
            pass


if __name__ == "__main__":
    main()