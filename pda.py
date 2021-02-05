from zipfile import ZipFile
import io
import re
from collections import namedtuple


PdaMessage = namedtuple('PdaMessage', ['round_id', 'timestamp', 'ckey', 'ic_name', 'to', 'message', 'location'])

def parse_roundstart_message(log_line):
    m = re.match(r'\[([^\]]+)\] Starting up round ID (\d+).', log_line)
    assert m, "Failed to parse roundstart message"
    return int(m.group(2))

def parse_divider_message(log_line):
    assert log_line.startswith(' - -------------------------')


def parse_pda_message(log_line):
    # [2020-09-23 00:25:48.511] PDA: alice/(Alice Alison) (PDA: �PDA to Bob Bobson (Assistant)) "hello" (Command Hallway (141,116,2))
    m = re.match(r'\[([^\]]+)\] PDA: (.+)/(.+) \(PDA: .* to (.+)\) \"(.+)\" \((.+)\)$', log_line)
    assert m, "Failed to parse manifest message: {}".format(log_line)
    return m.groups()

def parse_pda(stream):
    round_id = parse_roundstart_message(next(stream))
    parse_divider_message(next(stream))
    for log_line in stream:
        m = parse_pda_message(log_line)
        print(m)


def main():
    with ZipFile('data/month.2020-09.zip') as zf:
        with zf.open('02/round-145507/pda.txt', 'r') as fp:
            stream = io.TextIOWrapper(fp, 'utf-8')
            parse_pda(stream)


if __name__ == '__main__':
    main()