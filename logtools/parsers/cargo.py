import re
import logging
import datetime
import sys

from logtools.models import CargoShippedOrder
from logtools.parsers.base import BaseParser, RE_GAME_MESSAGE, ExternalInfo


LOG = logging.getLogger(__name__)


class CargoHtmlParser(BaseParser):

    log_filename = "cargo.html"

    def parse_stream(self, stream, external_info: ExternalInfo):
        round_id = external_info.round_id

        for line in stream:
            line = line.rstrip("\n")
            m = re.match(r"([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}) \[([^\]]+)\] \((.+?)\) \|\| (.*)", line)
            if not m:
                continue
            year, month, day, hour, minute, second, src, location, message = m.groups()
            dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
            m = re.search(r"Order #\d+ \((.+), placed by (.+)\), paid by (.+) has shipped.", message)
            if not m:
                LOG.warning("Can't parse %s", line)
                continue
            order, ordered_by, paid_by = m.groups()
            yield CargoShippedOrder(
                round_id=round_id,
                dt=dt,
                order=order,
                ordered_by=ordered_by,
                paid_by=paid_by,
            )