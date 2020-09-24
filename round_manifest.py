from zipfile import ZipFile
import io
import re
from collections import namedtuple


# WRITE_LOG(GLOB.world_manifest_log, "[ckey] \\ [body.real_name] \\ [mind.assigned_role] \\ [mind.special_role ? mind.special_role : "NONE"] \\ [latejoin ? "LATEJOIN":"ROUNDSTART"]")
#
# [2020-09-02 00:32:00.780] Starting up round ID 145507.
# - -------------------------
# [2020-09-02 00:35:37.585] skyhawk01138 \ Harry Stanton \ Station Engineer \ NONE \ ROUNDSTART
# [2020-09-02 00:35:38.233] rubyflamewing \ Takes-Two-Chairs \ Scientist \ NONE \ ROUNDSTART
# [2020-09-02 00:35:38.517] kinggoldcatter \ Brylon Overstreet \ Chief Medical Officer \ NONE \ ROUNDSTART 


ManifestEntry = namedtuple('ManifestEntry', ['round_id', 'timestamp', 'ckey', 'ic_name', 'assigned_role', 'special_role', 'status'])


def parse_roundstart_message(log_line):
    m = re.match(r'\[([^\]]+)\] Starting up round ID (\d+).', log_line)
    assert m, "Failed to parse manifest roundstart message"
    return int(m.group(2))

def parse_divider_message(log_line):
    assert log_line.startswith(' - -------------------------')

def parse_player_message(log_line):
    m = re.match(r'\[([^\]]+)\] (.+) \\ (.+) \\ (.+) \\ (.+) \\ (.+)$', log_line)
    assert m, "Failed to parse manifest message: {}".format(log_line)
    return m.groups()

def parse_manifest(manifest_txt_fp):
    round_id = parse_roundstart_message(next(manifest_txt_fp))
    parse_divider_message(next(manifest_txt_fp))
    print(round_id)
    for line in manifest_txt_fp:
        p = parse_player_message(line.rstrip('\n'))
        yield ManifestEntry(round_id, *p)


def main():
    with ZipFile('data/month.2020-09.zip') as zf:
        with zf.open('02/round-145507/manifest.txt', 'r') as fp:
            for msg in parse_manifest(io.TextIOWrapper(fp, 'utf-8')):
                print(msg)

if __name__ == '__main__':
    main()