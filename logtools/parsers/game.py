import re
import logging
import datetime

from logtools.models import Game, MetricsStruct
from logtools.parsers.base import BaseParser, RE_GAME_MESSAGE, ExternalInfo
from logtools.parsers.functions import parse_dt_string
from dataclasses import dataclass


LOG = logging.getLogger(__name__)

RE_GAME_SAY = re.compile(r"(.+?)/\((.+?)\) (?:\((.+?)\) )?(?:\((.+?)\) )?\"(.+?)\" (?:FORCED by (.+?) )?\((.+?)\)$")
RE_GAME_OOC = re.compile(r"(.+?)/\((.+?)\) \"(.+?)\" \((.+?)\)$")
RE_RUSSIAN_LETTERS = re.compile(r"[а-я]", re.UNICODE | re.IGNORECASE)

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

    >>> _parse_game_say('Carloszx/(Lisa Red) "captain of the damned" (Emergency Shuttle (144,155,13))')
    ('Carloszx', 'Lisa Red', None, None, 'captain of the damned', None, 'Emergency Shuttle (144,155,13)')
    """
    m = re.match(RE_GAME_SAY, message)
    if m:
        ckey, mob_name, mob_id, reason, text, forced, location = m.groups()
        if ckey == "*no key*":
            ckey = None
        return ckey, mob_name, mob_id, reason, text, forced, location
    return None


def _parse_game_ooc(message):
    """
    >>> _parse_game_ooc('FakeCkey/(Fake mob name) "i was the miiner" (start area (8,248,1))')
    ('FakeCkey', 'Fake mob name', 'i was the miiner', 'start area (8,248,1)')
    """
    if m := re.match(RE_GAME_OOC, message):
        ckey, mob_name, text, location = m.groups()
        if ckey == "*no key*":
            ckey = None
        return ckey, mob_name, text, location
    return None


def _contains_russian(text):
    """
    >>> _contains_russian("Asdfы")
    True
    >>> _contains_russian("Ж")
    True
    >>> _contains_russian("Hello")
    False
    """
    return bool(re.search(RE_RUSSIAN_LETTERS, text))


class GameTxtParser(BaseParser):

    log_filename = "game.txt"

    def parse_stream(self, stream, external_info: ExternalInfo, metrics: MetricsStruct):
        round_id = None

        for line in stream:
            line = line.rstrip('\n')
            if line.startswith(' -') or line.startswith('-'):
                continue
            
            metrics.total += 1
            m = re.match(RE_GAME_MESSAGE, line)
            if not m:
                metrics.failed += 1
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

            if category == "GAME-SAY" or category == "SAY":
                v = _parse_game_say(message)
                if v:
                    ckey, mob_name, mob_id, reason, text, forced, location = v

                    metrics.parsed += 1
                    yield Game, dict(
                        round_id=round_id,
                        category="GAME-SAY",
                        dt=dt,
                        ckey=ckey,
                        mob_name=mob_name,
                        mob_id=mob_id,
                        reason=reason,
                        text=text,
                        forced=forced,
                        location=location,
                        ru=_contains_russian(text),
                    )
                else:
                    metrics.failed += 1
                    LOG.error("Failed to parse GAME-SAY: %s", message)
                continue
            elif category == "GAME-OOC" or category == "OOC":
                v = _parse_game_ooc(message)
                if v:
                    ckey, mob_name, text, location = v

                    metrics.parsed += 1
                    yield Game, dict(
                        round_id=round_id,
                        category="GAME-OOC",
                        dt=dt,
                        ckey=ckey,
                        mob_name=mob_name,
                        mob_id=None,
                        reason=None,
                        text=text,
                        forced=None,
                        location=location,
                        ru=_contains_russian(text),
                    )
                else:
                    metrics.failed += 1
                    LOG.error("Failed to parse GAME-OOC: %s", message)
                continue
            else:
                metrics.skipped += 1
                continue