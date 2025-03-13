import datetime
import dataclasses
import random
import sqlite3
from pprint import pprint
import re
import logging
import os
import io
from zipfile import BadZipFile, ZipFile

import tqdm

from logtools.models import MetricsStruct
from logtools.parsers.game import RE_GAME_MESSAGE, _parse_game_ooc, _parse_game_say, _contains_russian

@dataclasses.dataclass
class Game:
    round_id: int
    category: str
    dt: datetime.datetime
    ckey: str
    mob_name: str
    mob_id: str
    reason: str
    prefix: str
    text: str
    forced: str
    location: str
    x: int
    y: int
    z: int
    ru: bool


logging.basicConfig(level=logging.CRITICAL, format='[%(asctime)s] - %(levelname)s - %(message)s')
LOG = logging.getLogger(__name__)


def get_sqlite_field_type(cls):
    if cls == int:
        return "INTEGER"
    elif cls == float:
        return "REAL"
    elif cls == str:
        return "TEXT"
    elif cls == datetime.datetime:
        return "DATETIME"
    elif cls == bool:
        return "BOOLEAN"
    else:
        raise TypeError(f"Type {cls} can't be matched to a SQLite type")


def infer_table_name(cls):
    return cls.__name__.lower()


def generate_create_table_query(cls, if_not_exists=False):
    columns_def = []
    for field in dataclasses.fields(cls):
        field_type = get_sqlite_field_type(field.type)
        columns_def.append(f"  {field.name} {field_type}")
    columns_def_str = ",\n".join(columns_def)
    table_name = infer_table_name(cls)
    if_not_exists_str = "IF NOT EXISTS " if if_not_exists else ""
    query = f"CREATE TABLE {if_not_exists_str}\"{table_name}\"\n(\n{columns_def_str}\n);"
    return query


def generate_drop_table_query(cls, if_exists=False):
    table_name = infer_table_name(cls)
    if_exists_str = "IF EXISTS " if if_exists else ""
    return f"DROP TABLE {if_exists_str}\"{table_name}\";"


def generate_insert_query(cls):
    table_name = infer_table_name(cls)
    num_fields = len(dataclasses.fields(cls))
    fields_placeholder = ",".join("?" * num_fields) 
    query = f"INSERT INTO \"{table_name}\" VALUES ({fields_placeholder});"
    return query


#@profile
def parse_stream(stream):
    round_id = None
    records = []

    for line in stream:
        line = line.rstrip('\n')
        if line.startswith(' -') or line.startswith('-'):
            continue
        
        m = re.match(RE_GAME_MESSAGE, line)
        if not m:
            LOG.warning("Can't parse %s", line)
            continue
        year, month, day, hour, minute, second, microsecond, category, message = m.groups()
        dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))

        if round_id is None:
            m = re.match(r"Round ID: (\d+)$", message)
            if m:
                round_id_str = m.group(1)
                if round_id is None:
                    round_id = int(round_id_str)
                continue

        if category == "GAME-SAY" or category == "SAY":
            v = _parse_game_say(message)
            if v:
                ckey, mob_name, mob_id, reason, prefix, text, forced, location, x, y, z = v

                records.append(Game(
                    round_id=round_id,
                    category="GAME-SAY",
                    dt=dt,
                    ckey=ckey,
                    mob_name=mob_name,
                    mob_id=mob_id,
                    reason=reason,
                    prefix=prefix,
                    text=text,
                    forced=forced,
                    location=location,
                    x=x,
                    y=y,
                    z=z,
                    ru=_contains_russian(text),
                ))
            else:
                LOG.error("Failed to parse GAME-SAY: %s", message)
            continue
        elif category == "GAME-OOC" or category == "OOC":
            v = _parse_game_ooc(message)
            if v:
                ckey, mob_name, text, location, x, y, z = v

                records.append(Game(
                    round_id=round_id,
                    category="GAME-OOC",
                    dt=dt,
                    ckey=ckey,
                    mob_name=mob_name,
                    mob_id=None,
                    reason=None,
                    prefix=None,
                    text=text,
                    forced=None,
                    location=location,
                    x=x,
                    y=y,
                    z=z,
                    ru=_contains_russian(text),
                ))
            else:
                LOG.error("Failed to parse GAME-OOC: %s", message)
            continue
        else:
            continue
    return records


#@profile
def parse_archive(directory, archive_filename, log_filename):
    try:
        with ZipFile(os.path.join(directory, archive_filename), "r") as zf:
            with zf.open(log_filename) as fp:
                stream = io.TextIOWrapper(fp, 'utf8')
                yield parse_stream(stream)
    except KeyError as exc:
        LOG.warning("Failed to open %s:%s - %s", archive_filename, log_filename, str(exc))
    except BadZipFile as exc:
        LOG.error("Failed to open %s - %s", archive_filename, str(exc))
    except Exception as exc:
        LOG.error("Failed to parse %s:%s - %s", archive_filename, log_filename, str(exc))
        raise


def sqlite_test():    
    con = sqlite3.connect("monkey.sqlite")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS junk(name)")
    data = ["1", "2", "3"]
    cur.executemany("INSERT INTO junk VALUES(?)", data)
    r = cur.execute("SELECT * FROM junk")
    print(r.fetchall())
    cur.execute("DROP TABLE junk")
    con.commit()
    con.close()


def get_random_sample(directory, sample=1):
    files = os.listdir(directory)
    return random.sample(files, k=sample)


def main():
    random.seed(69696969)
    directory = "logs"

    with sqlite3.connect("monkey.sqlite") as con:
        cur = con.cursor()

        query = generate_drop_table_query(Game, if_exists=True)
        cur.execute(query)

        query = generate_create_table_query(Game)
        cur.execute(query)

        query = generate_insert_query(Game)

        files = get_random_sample(directory, sample=1000)
        for filename in tqdm.tqdm(files):
            for record in parse_archive(directory, filename, "game.txt"):
                pass

        # cur.executemany(query, [dataclasses.astuple(sample)])

        r = cur.execute("SELECT * from game").fetchall()
        print(r)




if __name__ == "__main__":
    main()