import io
import logging
import os
import re
from dataclasses import dataclass, asdict
from zipfile import BadZipFile, ZipFile

from logtools.models import Metrics, MetricsStruct
LOG = logging.getLogger(__name__)

RE_DT = r"\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]{3})\]"
RE_GAME_MESSAGE = re.compile(RE_DT + r" (?:([A-Za-z- ]+): )?(.*)$")

@dataclass
class ExternalInfo:
    round_id: int


class BaseParser:

    log_filename = "__none__"

    def parse_stream(self, stream, external_info: ExternalInfo, metrics: MetricsStruct):
        raise NotImplementedError()

    def parse_file_from_archive(self, directory, archive_filename):
        try:
            with ZipFile(os.path.join(directory, archive_filename), "r") as zf:
                with zf.open(self.log_filename) as fp:
                    stream = io.TextIOWrapper(fp, 'utf8')
                    m = re.match(r"round-(\d+)\.zip", archive_filename)
                    round_id = int(m.group(1))
                    external_info = ExternalInfo(round_id=round_id)
                    metrics = MetricsStruct(
                        archive=archive_filename,
                        logfile=self.log_filename,
                    )
                    for record in self.parse_stream(stream, external_info, metrics):
                        yield record
                    yield Metrics, asdict(metrics)
        except KeyError as exc:
            LOG.warn("Failed to open %s:%s - %s", archive_filename, self.log_filename, str(exc))
        except BadZipFile as exc:
            LOG.error("Failed to open %s - %s", archive_filename, str(exc))
        except Exception as exc:
            LOG.error("Failed to parse %s:%s - %s", archive_filename, self.log_filename, str(exc))
            raise


class _Skip:
    
    def __repr__(self):
        return "Skip"


Skip = _Skip()