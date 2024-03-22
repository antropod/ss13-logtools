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


def get_ckey_rounds(ckey):
    records = (
        Session()
        .query(Manifest)
        .filter(Manifest.ckey==ckey)
        .order_by(Manifest.round_id)
        .all()
    )
    return [r.round_id for r in records]


def main():
    rounds = get_ckey_rounds("")
    round_id = rounds[0]
    LOG.info("parsing round %s", round_id)
    filename = f"round-{round_id}.zip"

    parser = GameTxtParser()
    records = parser.parse_file_from_archive("logs", filename)
    # for r in records:
    #     print(r.category, r.subcategory, r.message)


if __name__ == "__main__":
    main()