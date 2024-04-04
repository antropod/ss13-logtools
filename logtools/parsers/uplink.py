import re
import logging
import sys

from logtools.models.uplink import Uplink, Changeling, Spell
from logtools.parsers.base import BaseParser, RE_GAME_MESSAGE, Skip
from logtools.parsers.functions import parse_dt_string, nullable_int
import datetime
from logtools.parsers.functions import nullable_int

LOG = logging.getLogger(__name__)

RE_UPLINK_PURCHASE = re.compile(r"(.+?)/\((.+?)\) purchased (.+?) (?:\((\d+)% off!\) )?for (\d+) telecrystals from (?:ï¿½)?(.*)'s uplink$")
RE_UPLINK_LOAD_TC = re.compile(r"(.+?)/\((.+?)\) loaded (\d+) telecrystals into .+ uplink$")
RE_UPLINK_RANDOM_ITEM = re.compile(r"(.+?)/\((.+?)\) purchased a random uplink item from .+ uplink with (\d+) telecrystals remaining$")


def _parse_uplink(message):
    """
    >>> _parse_uplink("RandomCkey/(Random Clown Name) purchased Banana Cream Pie Cannon for 10 telecrystals from Random Clown Name (Clown)'s uplink")
    ('RandomCkey', 'Random Clown Name', 'Banana Cream Pie Cannon', None, '10', 'Random Clown Name (Clown)')

    >>> _parse_uplink("RandomCkey/(Random Name) purchased Super Pointy Tape for 1 telecrystals from 's uplink")
    ('RandomCkey', 'Random Name', 'Super Pointy Tape', None, '1', '')

    >>> _parse_uplink("RandomCkey/(Random Name) purchased Radioactive Microlaser (33% off!) for 2 telecrystals from the uplink implant's uplink")
    ('RandomCkey', 'Random Name', 'Radioactive Microlaser', '33', '2', 'the uplink implant')

    >>> _parse_uplink("RandomCKey/(Random Name) loaded 1 telecrystals into the station bounced radio's uplink")
    Skip

    >>> _parse_uplink("Germo555/(Zee-Lanp) purchased a random uplink item from Zee-Lanp's uplink with 2 telecrystals remaining")
    Skip
    """
    m = RE_UPLINK_PURCHASE.match(message)
    if m:
        return m.groups()
    m = RE_UPLINK_LOAD_TC.match(message)
    if m:
        return Skip
    m = RE_UPLINK_RANDOM_ITEM.match(message)
    if m:
        return Skip
    return None


def _guess_uplink_type(uplink_name):
    if '(' in uplink_name and ')' in uplink_name or 'PDA' in uplink_name:
        return "pda"
    elif "station bounced radio" in uplink_name:
        return "nukeops"
    elif "uplink implant" in uplink_name:
        return "implant"
    elif 'pen' in uplink_name:
        return "pen"
    elif 'headset' in uplink_name:
        return "headset"
    elif uplink_name == '':
        return "unknown"
    elif "debug" in uplink_name:
        return "debug"
    else:
        LOG.warning("Unknown uplink type: %s", uplink_name)


RE_CHANGELING_ADAPT = re.compile(r"(.+?)/\((.+?)\) adapted the (.+) power$")
RE_CHANGELING_READAPT = re.compile(r"(.+?)/\((.+?)\) readapted their changeling powers$")

def _parse_changeling(message):
    """
    >>> _parse_changeling("RandomCKey/(Random Name) adapted the Anatomic Panacea power")
    ('RandomCKey', 'Random Name', 'Anatomic Panacea')

    >>> _parse_changeling("Livrah/(Boris Mahnov) readapted their changeling powers")
    ('Livrah', 'Boris Mahnov', 'READAPTED')
    """
    if m:= re.match(RE_CHANGELING_ADAPT, message):
        return m.groups()
    if m:= re.match(RE_CHANGELING_READAPT, message):
        return m.groups() + ("READAPTED",)
    return None


RE_SPELL = re.compile(r"(.+?)/\((.+?)\) (?:learned|bought|cast|refunded) (.+) for (\d+) points$")
RE_SPELL_UPGRADE = re.compile(r"(.+?)/\((.+?)\) improved their knowledge of (.+) to level (\d+) for (\d+) points$")

def _parse_spell(message):
    """
    >>> _parse_spell("UwUer/(Lumi The White) learned Rod Form for 2 points")
    ('UwUer', 'Lumi The White', 'Rod Form', '2')
    >>> _parse_spell("Goblinman221/(Granddalf The Daddest) improved their knowledge of Forcewall to level 2 for 1 points")
    Skip
    """
    if m:= re.match(RE_SPELL, message):
        return m.groups()
    if m:= re.match(RE_SPELL_UPGRADE, message):
        return Skip

class UplinkTxtParser(BaseParser):

    log_filename = "uplink.txt"

    def parse_stream(self, stream):
        header = next(stream)
        m = re.match(r'\[([^\]]+)\] Starting up round ID (\d+).', header)
        _, round_id = m.groups()
        round_id = int(round_id)

        for line in stream:
            line = line.rstrip('\n')
            if line.startswith(' -'):
                continue
            m = re.match(RE_GAME_MESSAGE, line)
            if not m:
                LOG.warning("Can't parse %s", line)
                continue
            year, month, day, hour, minute, second, microsecond, category, message = m.groups()
            dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))
            if category == "UPLINK":
                r = _parse_uplink(message)
                if r is Skip:
                    continue
                if r and len(r) == 6:
                    ckey, name, item, discount, price, uplink_name = r
                    uplink_type=_guess_uplink_type(uplink_name)

                    yield Uplink(
                        round_id=round_id,
                        dt=dt,
                        ckey=ckey,
                        name=name,
                        item=item,
                        discount=nullable_int(discount),
                        price=nullable_int(price),
                        uplink_type=uplink_type,
                    )
                else:
                    LOG.warning("Can't parse %s", line)

            elif category == "UPLINK-CHANGELING":
                r = _parse_changeling(message)
                if r:
                    ckey, name, power = r
                    yield Changeling(
                        round_id=round_id,
                        dt=dt,
                        ckey=ckey,
                        name=name,
                        power=power,
                    )
                else:
                    LOG.warning("Can't parse %s", line)

            elif category == "UPLINK-SPELL":
                r = _parse_spell(message)
                if r:
                    if r is Skip:
                        continue
                    ckey, name, spell, price = r
                    yield Spell(
                        round_id=round_id,
                        dt=dt,
                        ckey=ckey,
                        name=name,
                        spell=spell,
                        price=price,
                    )
                else:
                    LOG.warning("Can't parse %s", line)
                    sys.exit(0)
            elif category == "UPLINK-HERETIC":
                pass
            elif category == "UPLINK-MALF":
                pass
            elif category == "UPLINK-SPY":
                pass
            else:
                LOG.warning("Can't parse %s", line)
                continue
