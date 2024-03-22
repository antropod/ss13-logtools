import re
import logging
import datetime

#from logtools.models.manifest import Game
from logtools.parsers.base import BaseParser
from logtools.parsers.functions import parse_dt_string
from dataclasses import dataclass


LOG = logging.getLogger(__name__)

@dataclass
class Game:
    round_id: int
    dt: datetime.datetime
    category: str
    subcategory: str
    message: str


class GameTxtParser(BaseParser):

    log_filename = "game.txt"

    def parse_stream(self, stream):
        round_id = None

        for line in stream:
            line = line.rstrip('\n')
            if line.startswith(' -') or line.startswith('-'):
                continue

            m = re.match(r"\[([^\]]+)\] ([A-Za-z-]+): (.*)$", line)
            if not m:
                LOG.warning("Can't parse %s", line)
                continue
            dt, category, message = m.groups()

            if round_id is None:
                m = re.match(r"Round ID: (\d+)$", message)
                if m:
                    round_id_str = m.group(1)
                    if round_id is None:
                        round_id = int(round_id_str)
                    continue

            m = re.match(r"([^:]+): (.*)$", message)
            if m:
                subcategory, message = m.groups()
            else:
                subcategory = None

            yield Game(
                round_id=round_id,
                dt=parse_dt_string(dt),
                category=category,
                subcategory=subcategory,
                message=message
            )