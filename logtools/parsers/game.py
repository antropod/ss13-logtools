import re
import logging
import datetime

from logtools.models.game import GameSay
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

            if category == "GAME-SAY":
                m = re.match(r"([^/]+)/\(([^()]+(?:\([^)]+\))?)\) \(([^)]+)\) (?:\(([^)]+)\) )?\"([^\"]+)\" (FORCED by [^(]+ )?\((.*)\)$", message)
                if m:
                    ckey, mob_name, mob_id, reason, text, forced, location = m.groups()
                    if ckey == "*no key*":
                        ckey = None

                    yield GameSay(
                        round_id=round_id,
                        dt=parse_dt_string(dt),
                        ckey=ckey,
                        mob_name=mob_name,
                        mob_id=mob_id,
                        reason=reason,
                        text=text,
                        forced=forced,
                        location=location,
                    )
                else:
                    LOG.error("Failed to parse GAME-SAY: %s", message)
                continue

            # m = re.match(r"([^:]+): (.*)$", message)
            # if m:
            #     subcategory, message = m.groups()
            # else:
            #     subcategory = None

            # yield Game(
            #     round_id=round_id,
            #     dt=parse_dt_string(dt),
            #     category=category,
            #     subcategory=subcategory,
            #     message=message
            # )