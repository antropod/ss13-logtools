import re
import logging

from logtools.models.uplink import Uplink, Changeling
from logtools.parsers.base import BaseParser
from logtools.parsers.functions import parse_dt_string, nullable_int


LOG = logging.getLogger(__name__)

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
            m = re.match(r"\[([^\]]+)\] ([^:]+): ([^/]+)/\((.+)\) ((?:purchased|adapted) .*)$", line)
            if not m:
                LOG.warning("Can't parse %s", line)
                continue
            dt, type_, ckey, name, message = m.groups()
            dt = parse_dt_string(dt)
            if type_ == "UPLINK":
                m = re.match(r"purchased (.+?)(?: \(([\d]+)% off!\))? for (\d+) telecrystals from (.*)'s uplink$", message)
                if not m:
                    LOG.warning("Can't parse \"%s\"", message)
                    continue

                item, discount, price, _source = m.groups()

                yield Uplink(
                    round_id=round_id,
                    dt=dt,
                    ckey=ckey,
                    name=name,
                    item=item,
                    discount=nullable_int(discount),
                    price=int(price),
                )
            elif type_ == "UPLINK-CHANGELING" or type_ == "CHANGELING":
                m = re.match(r"adapted the (.+?) power$", message)
                if not m:
                    LOG.warning("Can't parse \"%s\"", message)
                    continue
                power, = m.groups()
                yield Changeling(
                    round_id=round_id,
                    dt=dt,
                    ckey=ckey,
                    name=name,
                    power=power
                )
            else:
                LOG.warning("Message type: \"%s\" is not supported", type_)
                continue
