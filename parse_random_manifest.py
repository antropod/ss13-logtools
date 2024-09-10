import os
import random
from common import Session

from logtools.parsers.manifest import ManifestTxtParser


def get_random_log(directory):
    files = os.listdir(directory)
    return random.choice(files)


def main():
    filename = get_random_log("logs")
    parser = ManifestTxtParser()
    records = parser.parse_archive("logs", filename)
    for r in records:
        print(r)


if __name__ == "__main__":
    main()