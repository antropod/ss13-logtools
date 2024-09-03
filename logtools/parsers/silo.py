import re
import logging
import datetime
import sys

from logtools.models import Silo, MetricsStruct
from logtools.parsers.base import BaseParser, RE_GAME_MESSAGE, ExternalInfo


LOG = logging.getLogger(__name__)


def parse_material_string(s):
    """
    >>> parse_material_string('-250 iron, -125 glass')
    {'iron': -250, 'glass': -125}
    """
    result = {}
    for m in s.split(", "):
        amount, material = m.split(" ", maxsplit=1)
        result[material.replace(" ", "_")] = int(amount)
    return result


def parse_silo(message):
    """
    >>> parse_silo("department techfab (Medical) in [Medbay Storage (152,101,4)] built 1x Bonesetter | -250 iron, -125 glass")
    ('department techfab (Medical)', 'Medbay Storage (152,101,4)', 'built', 1, 'Bonesetter', {'iron': -250, 'glass': -125})

    >>> parse_silo("ore redemption machine in [Cargo Office (90,116,4)] deposited 100x sand pile | +100 glass")
    ('ore redemption machine', 'Cargo Office (90,116,4)', 'deposited', 100, 'sand pile', {'glass': 100})

    >>> parse_silo("ore redemption machine in [Cargo Office (90,116,4)] deposited 1100x bluespace crystal | +1100 bluespace crystal")
    ('ore redemption machine', 'Cargo Office (90,116,4)', 'deposited', 1100, 'bluespace crystal', {'bluespace_crystal': 1100})
    """
    m = re.match(r"(.*) in \[(.*)\] (\S+) (\d+)x (.+) \| (.*)$", message)
    if m:
        machine, loc, action, amount, item, materials_string = m.groups()
        materials = parse_material_string(materials_string)
        amount = int(amount)
        return machine, loc, action, amount, item, materials
    return None


class SiloParser(BaseParser):

    log_filename = "silo.txt"

    def parse_stream(self, stream, external_info: ExternalInfo, metrics: MetricsStruct):
        header = next(stream)
        m = re.search(r'Starting up round ID (\d+).', header)
        round_id = int(m.group(1))

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
            r = parse_silo(message)
            if r:
                machine, loc, action, amount, item, materials = r
                yield Silo, dict(
                    round_id=round_id,
                    dt=dt,
                    machine=machine,
                    loc=loc,
                    action=action,
                    amount=amount,
                    item=item,
                    **materials,
                )
            else:
                LOG.warning("Can't parse %s", line)