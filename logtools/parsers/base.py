import logging
from zipfile import ZipFile, BadZipFile
import io
import os

LOG = logging.getLogger(__name__)


class BaseParser:

    log_filename = "__none__"

    def parse_stream(stream):
        raise NotImplementedError()

    def parse_file_from_archive(self, directory, archive_filename):
        try:
            with ZipFile(os.path.join(directory, archive_filename), "r") as zf:        
                with zf.open(self.log_filename) as fp:
                    stream = io.TextIOWrapper(fp, 'latin-1')
                    for record in self.parse_stream(stream):
                        yield record
        except KeyError as exc:
            LOG.error("Failed to open %s:%s - %s", archive_filename, self.log_filename, str(exc))
        except BadZipFile as exc:
            LOG.error("Failed to open %s - %s", archive_filename, str(exc))
