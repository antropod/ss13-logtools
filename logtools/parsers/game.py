import re
import logging
import datetime

from logtools.models import GameSay
from logtools.parsers.base import BaseParser, RE_GAME_MESSAGE, ExternalInfo
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


RE_GAME_SAY = re.compile(r"(.+?)/\((.+?)\) \((.+?)\) (?:\((.+?)\) )?\"(.+?)\" (?:FORCED by (.+?) )?\((.+?)\)$")

def _parse_game_say(message):
    """
    >>> _parse_game_say('RandomCkey/(Random Mob) (mob_3156) "AAAAAAAAAA" (AI Chamber (150,25,4))')
    ('RandomCkey', 'Random Mob', 'mob_3156', None, 'AAAAAAAAAA', None, 'AI Chamber (150,25,4)')

    >>> _parse_game_say('RandomCkey/(Random Mob) (mob_3156) (VOX Announcement) "vox_login" (AI Chamber (150,25,4))')
    ('RandomCkey', 'Random Mob', 'mob_3156', 'VOX Announcement', 'vox_login', None, 'AI Chamber (150,25,4)')

    >>> _parse_game_say('*no key*/(snow legion) (mob_456) "Why...?" FORCED by AI Controller (Icemoon Caves (255,218,3))')
    (None, 'snow legion', 'mob_456', None, 'Why...?', 'AI Controller', 'Icemoon Caves (255,218,3)')

    >>> _parse_game_say('ToastGoats/(D.A.N.I.E.L) (mob_3381) (HOLOPAD in Captains Office (84,132,3)) "Yes hello" (AI Chamber (190,36,3))')
    ('ToastGoats', 'D.A.N.I.E.L', 'mob_3381', 'HOLOPAD in Captains Office (84,132,3)', 'Yes hello', None, 'AI Chamber (190,36,3)')
    """
    m = re.match(RE_GAME_SAY, message)
    if m:
        ckey, mob_name, mob_id, reason, text, forced, location = m.groups()
        if ckey == "*no key*":
            ckey = None
        return ckey, mob_name, mob_id, reason, text, forced, location
    return None


class GameTxtParser(BaseParser):

    log_filename = "game.txt"

    def parse_stream(self, stream, external_info: ExternalInfo):
        round_id = None

        for line in stream:
            line = line.rstrip('\n')
            if line.startswith(' -') or line.startswith('-'):
                continue

            m = re.match(RE_GAME_MESSAGE, line)
            if not m:
                LOG.warning("Can't parse %s", line)
                continue
            year, month, day, hour, minute, second, microsecond, category, message = m.groups()
            dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))

            if round_id is None:
                m = re.match(r"Round ID: (\d+)$", message)
                if m:
                    round_id_str = m.group(1)
                    if round_id is None:
                        round_id = int(round_id_str)
                    continue

            if category == "GAME-SAY":
                v = _parse_game_say(message)
                if v:
                    ckey, mob_name, mob_id, reason, text, forced, location = v

                    yield GameSay, dict(
                        round_id=round_id,
                        dt=dt,
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
