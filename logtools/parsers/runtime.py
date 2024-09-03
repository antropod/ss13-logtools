import re
import logging
import datetime

from logtools.parsers.base import BaseParser, RE_GAME_MESSAGE, RE_DT, ExternalInfo
from logtools.parsers.functions import parse_dt_string
from logtools.models import MapInfo, MetricsStruct
from dataclasses import dataclass


LOG = logging.getLogger(__name__)


class RuntimeTxtParser(BaseParser):
    
    log_filename = "runtime.txt"
    
    def parse_stream(self, stream, external_info: ExternalInfo, metrics: MetricsStruct):
        round_id = None
        map_name = None
        round_start = None

        for line in stream:
            line = line.rstrip('\n')
            if line.startswith(' -') or line.startswith('-'):
                continue

            metrics.total += 1

            if round_id is None:
                m = re.match(RE_DT + r" Starting up round ID (\d+)\.$", line)
                if m:
                    year, month, day, hour, minute, second, microsecond, round_id_str = m.groups()
                    dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))
                    round_id = int(round_id_str)
                    round_start = dt
                    continue

            m = re.match(RE_GAME_MESSAGE, line)
            if not m:
                metrics.failed += 1
                LOG.warning("Can't parse %s", line)
                continue
            year, month, day, hour, minute, second, microsecond, category, message = m.groups()
            dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))

            if category != "RUNTIME":
                metrics.skipped += 1
                continue
            
            if map_name is None:
                m = re.match(r"Loading (.*)\.\.\.", message)
                if m:
                    map_name = m.groups()[0]
                    break
        # For this file metrics actually do not mean anything useful
        metrics.parsed += 1
        yield MapInfo, dict(
            round_id=round_id,
            map_name=map_name,
            dt=round_start
        )