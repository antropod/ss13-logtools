import re
import logging

from logtools.models import RoundEndData, MetricsStruct
from logtools.parsers.base import BaseParser, ExternalInfo
from bs4 import BeautifulSoup


LOG = logging.getLogger(__name__)
RE_OPERATIVES = re.compile(r"^.*Operatives:$")
RE_STATION_INTEGRITY = re.compile(r"Station Integrity")
RE_INTEGRITY_PERCENT = re.compile(r"(\S+)%")


class RoundEndDataHtmlParser(BaseParser):

    log_filename = "round_end_data.html"

    def parse_stream(self, stream, external_info: ExternalInfo, metrics: MetricsStruct):
        soup = BeautifulSoup(stream, 'html.parser')

        # nukies https://github.com/tgstation/tgstation/blob/da5db54b13b905e4e248ced95fdb0c75b5b70018/code/modules/antagonists/nukeop/datums/operative_team.dm#L28
        nukeop_result = None
        for tag in soup.find_all("span", string=RE_OPERATIVES, limit=1):
            nukeop_result = tag.next_sibling.next_sibling.text
        station_integrity = None
        station_destroyed = False
        for tag in soup.find_all(string=RE_STATION_INTEGRITY, limit=1):
            integrity_str = tag.next.text
            if m := re.match(RE_INTEGRITY_PERCENT, integrity_str):
                station_integrity = float(m.group(1))
            if integrity_str == 'Destroyed':
                station_integrity = 0
                station_destroyed = True

        metrics.total += 1
        metrics.parsed += 1
        yield RoundEndData, dict(
            round_id=external_info.round_id,
            nukeop_result=nukeop_result,
            station_integrity=station_integrity,
            station_destroyed=station_destroyed,
        )