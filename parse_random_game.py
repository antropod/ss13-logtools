import os
import random
from common import Session
import logging

from logtools.parsers.game import GameTxtParser
from logtools.parsers.runtime import RuntimeTxtParser
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
    parser = RuntimeTxtParser()
    filename = get_random_log("logs")

    records = parser.parse_file_from_archive("logs", filename)
    for r in records:
        print(r)


if __name__ == "__main__":
    main()