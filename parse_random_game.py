import os
import random
from common import Session
import logging

from logtools.parsers.game import GameTxtParser
from logtools.models.manifest import Manifest

logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)


def get_random_log(directory):
    files = os.listdir(directory)
    return random.choice(files)


def main():
    filename = get_random_log("logs")

    parser = GameTxtParser()
    records = parser.parse_file_from_archive("logs", filename)
    for r in records:
        if r.category == "GAME-SAY":
            print(r)
            pass


if __name__ == "__main__":
    main()