from logtools.models.uplink import Uplink, Changeling

import re
import logging
from zipfile import ZipFile, BadZipFile
import io
import os

from collections import namedtuple
import datetime

LOG = logging.getLogger(__name__)


def nullable_int(x):
    if x is None:
        return None
    return int(x)

def parse_dt_string(dt_string):
    return datetime.datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S.%f")


class UplinkTxtParser:

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
            elif type_ == "CHANGELING":
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
