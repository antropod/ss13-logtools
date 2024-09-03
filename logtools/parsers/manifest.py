import re
import logging

from logtools.models import Manifest, MetricsStruct
from logtools.parsers.base import BaseParser, ExternalInfo
from logtools.parsers.functions import parse_dt_string


LOG = logging.getLogger(__name__)


class ManifestTxtParser(BaseParser):

    log_filename = "manifest.txt"

    def parse_stream(self, stream, external_info: ExternalInfo, metrics: MetricsStruct):
        header = next(stream)
        m = re.search(r'Starting up round ID (\d+).', header)
        round_id = int(m.group(1))

        for line in stream:
            line = line.rstrip('\n')
            if line.startswith(' -'):
                continue
            m = re.match(r"\[([^\]]+)\] MANIFEST: (.+?) \\ (.+?) \\ (.+?) \\ (.+?) \\ (.+?)$", line)
            if not m:
                LOG.warning("Can't parse %s", line)
                continue

            dt, ckey, name, assigned_role, special_role, latejoin = m.groups()
            yield Manifest, dict(
                round_id=round_id,
                dt=parse_dt_string(dt),
                ckey=ckey,
                name=name,
                assigned_role=assigned_role,
                special_role=special_role if special_role != 'NONE' else None,
                latejoin=latejoin,
            )