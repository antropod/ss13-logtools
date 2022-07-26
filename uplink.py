import re
import logging
from zipfile import ZipFile
import io

from collections import namedtuple


logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)


def parse_uplink_txt(stream):
    header = next(stream)
    m = re.match(r'\[([^\]]+)\] Starting up round ID (\d+).', header)
    _, round_id = m.groups()
    round_id = int(round_id)

    for line in stream:
        line = line.rstrip('\n')
        if line.startswith(' -'):
            continue
        m = re.match(r"\[([^\]]+)\] ([^:]+): ([^/]+)/\(([^)]+)\) (.*)$", line)
        if not m:
            LOG.warning("Can't parse %s", line)
            continue
        dt, type_, ckey, name, message = m.groups()
        if type_ != "UPLINK":
            LOG.warning("Message type: %s is not supported", type_)
            continue

        m = re.match(r"purchased (.+?)(?: \(([\d]+)% off!\))? for (\d+) telecrystals from (.*)'s uplink$", message)
        if not m:
            LOG.warning("Can't parse message \"%s\"", message)
            continue

        item, discount, price, source = m.groups()

        yield dt, type_, ckey, name, item, discount, price, source


def main():
    with ZipFile("logs_2022/round-187172.zip", "r") as zf:
        with zf.open('uplink.txt') as fp:
            stream = io.TextIOWrapper(fp, 'latin-1')
            for line in parse_uplink_txt(stream):
                print(line)


if __name__ == "__main__":
    main()