from collections import namedtuple
from zipfile import ZipFile
import io
import logging
import re
import sys

logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)

GameMessage = namedtuple('GameMessage', 'round_id dt type message')


def parse_game_txt(stream):
    header = next(stream)
    m = re.match(r'\[([^\]]+)\] Starting up round ID (\d+).', header)
    _, round_id = m.groups()
    round_id = int(round_id)

    for line in stream:
        line = line.rstrip('\n')
        if line.startswith('-'):
            continue
        m = re.match(r'\[([^\]]+)\] ([^:]+): (.+$)', line)
        if m:
            dt, type_, message = m.groups()
            yield GameMessage(round_id, dt, type_, message)
        else:
            LOG.warning("Can't parse %s", line)


def parse_round_archive(filename):
    with ZipFile(filename, 'r') as zf:
        with zf.open('game.txt') as fp:
            stream = io.TextIOWrapper(fp, 'latin-1')
            for m in parse_game_txt(stream):
                yield m


def main():
    for m in parse_round_archive('data/round-155420.zip'):
        print(m)


if __name__ == '__main__':
    main()