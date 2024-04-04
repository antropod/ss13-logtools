import os
import random
from common import Session
import logging

from logtools.parsers.game import GameTxtParser
from logtools.parsers.runtime import RuntimeTxtParser
from logtools.models.manifest import Manifest
from logtools.parsers.uplink import UplinkTxtParser

logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)


def get_random_log(directory):
    files = os.listdir(directory)
    return random.choice(files)


def get_sample_logs(directory):
    files = os.listdir(directory)[:100]
    return files


def main():
    parser = UplinkTxtParser()
    filename = get_random_log("logs")

    records = parser.parse_file_from_archive("logs", filename)
    for r in records:
        pass


if __name__ == "__main__":
    main()