from zipfile import ZipFile
import io
import re
from collections import namedtuple
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)


ManifestEntry = namedtuple('ManifestEntry', ['round_id', 'timestamp', 'ckey', 'ic_name', 'assigned_role', 'special_role', 'status'])


def parse_roundstart_message(log_line):
    m = re.match(r'\[([^\]]+)\] Starting up round ID (\d+).', log_line)
    assert m, "Failed to parse roundstart message"
    return int(m.group(2))


def parse_divider_message(log_line):
    assert log_line.startswith(' - -------------------------')


def parse_player_message(log_line):
    m = re.match(r'\[([^\]]+)\] (.+) \\ (.+) \\ (.+) \\ (.+) \\ (.+)$', log_line)
    if not m:
        LOG.warning("Failed to parse manifest message: {}".format(log_line))
        return None
    return m.groups()


def parse_manifest(stream):
    round_id = parse_roundstart_message(next(stream))
    parse_divider_message(next(stream))
    for line in stream:
        p = parse_player_message(line.rstrip('\n'))
        if p:
            yield ManifestEntry(round_id, *p)


def iterate_round_files(arch_filename, log_name):
    with ZipFile(arch_filename, 'r') as zf:
        for zi in zf.infolist():
            if zi.filename.endswith(log_name):
                with zf.open(zi.filename) as fp:
                    yield fp


def parse_all_manifests(arch_filename):
    for fp in iterate_round_files(arch_filename, 'manifest.txt'):
        for msg in parse_manifest(io.TextIOWrapper(fp, 'utf-8')):
            yield msg


def department(assigned_role):
    return {
        'Assistant': 'Greytide',
        'Quartermaster': 'Supply',
        'Cargo Technician': 'Supply',
        'Shaft Miner': 'Supply',
        'Cook': 'Service',
        'Chaplain': 'Service',
        'Curator': 'Service',
        'Janitor': 'Service',
        'Prisoner': 'Prisoner',
        'Security Officer': 'Security',
        'Warden': 'Security',
        'Detective': 'Security',
        'Scientist': 'Science',
        'Head of Security': 'Command',
        'Paramedic': 'Medical',
        'Medical Doctor': 'Medical',
        'Chemist': 'Medical',
        'Atmospheric Technician': 'Engineering',
        'Station Engineer': 'Engineering',
        'Cyborg': 'Silicon',
        'AI': 'Silicon',
        'Bartender': 'Service',
        'Chief Engineer': 'Command',
        'Botanist': 'Service',
        'Geneticist': 'Science',
        'Roboticist': 'Science',
    }[assigned_role]


def main():
    messages = list(parse_all_manifests('data/month.2020-09.zip'))

    df = pd.DataFrame(messages)
    df.to_excel('manifest.xlsx')

    syndie_roles = ['Admiral', 'Genetics Researcher']
    special_rounds = df.loc[df.assigned_role.isin(syndie_roles)].round_id.unique()
    df['greytider'] = df.assigned_role == 'Assistant'
    df.loc[~df.round_id.isin(special_rounds)].groupby(['round_id', 'greytider'])['round_id'].count().unstack(-1).to_excel('job_stat.xlsx')


if __name__ == '__main__':
    main()