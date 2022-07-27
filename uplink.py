import re
import logging
from zipfile import ZipFile
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


def parse_uplink_txt(stream):
    header = next(stream)
    m = re.match(r'\[([^\]]+)\] Starting up round ID (\d+).', header)
    _, round_id = m.groups()
    round_id = int(round_id)

    for line in stream:
        line = line.rstrip('\n')
        if line.startswith(' -'):
            continue
        m = re.match(r"\[([^\]]+)\] ([^:]+): ([^/]+)/\((.+)\) (purchased .*)$", line)
        if not m:
            LOG.warning("Can't parse %s", line)
            continue
        dt, type_, ckey, name, message = m.groups()
        if type_ != "UPLINK":
            LOG.warning("Message type: %s is not supported", type_)
            continue

        m = re.match(r"purchased (.+?)(?: \(([\d]+)% off!\))? for (\d+) telecrystals from (.*)'s uplink$", message)
        if not m:
            LOG.warning("Can't parse \"%s\"", message)
            continue

        item, discount, price, source = m.groups()

        yield round_id, parse_dt_string(dt), type_, ckey, name, item, nullable_int(discount), int(price), source


def parse_from_archive(directory, archive_filename, log_filename):
    with ZipFile(os.path.join(directory, archive_filename), "r") as zf:
        try:
            with zf.open(log_filename) as fp:
                stream = io.TextIOWrapper(fp, 'latin-1')
                for record in parse_uplink_txt(stream):
                    yield record
        except KeyError as exc:
            LOG.error("Failed to open %s: %s", archive_filename, str(exc))


def main():
    for record in parse_from_archive("logs_2022", "round-186148.zip", "uplink.txt"):
        print(record)


if __name__ == "__main__":
    main()