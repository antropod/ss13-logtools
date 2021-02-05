import re
from zipfile import ZipFile
import io
import logging
from collections import namedtuple

logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)

GameMessage = namedtuple('GameMessage', 'dt type message')


def parse_game_txt(stream):
    for line in stream:
        line = line.rstrip('\n')
        if line.startswith('-'):
            continue
        m = re.match(r'\[([^\]]+)\] ([^:]+): (.+$)', line)
        if m:
            yield GameMessage(*m.groups())
        else:
            LOG.warning("Can't parse %s", line)


def parse_round_archive(filename):
    with ZipFile(filename, 'r') as zf:
        with zf.open('game.txt') as fp:
            stream = io.TextIOWrapper(fp, 'utf-8')
            for m in parse_game_txt(stream):
                yield m


def main():
    for m in parse_round_archive('data/round/round-153311.zip'):
        print(repr(m))


if __name__ == '__main__':
    main()