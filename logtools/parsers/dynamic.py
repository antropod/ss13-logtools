import re
import logging
import json

from dataclasses import asdict
import datetime

from logtools.models import Dynamic, DynamicStruct, MetricsStruct, Metrics
from logtools.parsers.base import BaseParser, ExternalInfo, RE_GAME_MESSAGE
from logtools.parsers.functions import parse_dt_string


LOG = logging.getLogger(__name__)

# def _game_message_works(line):
#     """
#     >>> _game_message_works('[2023-04-17 23:55:41.426] DYNAMIC: Dynamic mode parameters for the round:')
#     """
#     return re.match(RE_GAME_MESSAGE, line)


class DynamicTxtParser(BaseParser):

    log_filename = "dynamic.txt"

    def parse_stream(self, stream, external_info: ExternalInfo, metrics: MetricsStruct):
        result = DynamicStruct(round_id=external_info.round_id, dt_start=None)

        header = next(stream)
        m = re.match(r'\[([^\]]+)\] Starting up round ID (\d+).', header)
        if m:
            dt_start, round_id = m.groups()
            result.round_id = int(round_id)
            result.dt_start = parse_dt_string(dt_start)

        for line in stream:
            line = line.rstrip('\n')
            if line.startswith(' -'):
                continue

            m = re.match(RE_GAME_MESSAGE, line)
            if not m:
                LOG.warning("Can't parse %s", line)
                continue
            year, month, day, hour, minute, second, microsecond, category, message = m.groups()
            if result.dt_start is None:
                result.dt_start = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))

            if category == "DYNAMIC":
                if m:= re.match(r"Listing \d+ round start rulesets, and (\d+) players ready\.$", message):
                    result.players_ready = int(m.group(1))
                elif m:= re.match(r"Dynamic Mode initialized with a Threat Level of\.\.\. (\S+)! \((\S+) round start budget\)$", message):
                    result.threat_level = float(m.group(1))
                    result.round_start_budget = float(m.group(2))
                else:
                    pass
            else:
                LOG.warning("Unknown category %s at %s", category, line)

        metrics.total += 1
        if result.is_filled():
            metrics.parsed += 1
        else:
            metrics.failed += 1
        yield Dynamic, asdict(result)


class DynamicJsonParser(BaseParser):

    log_filename = "dynamic.json"

    def parse_stream(self, stream, external_info: ExternalInfo, metrics: MetricsStruct):
        result = DynamicStruct(
            round_id=external_info.round_id,
            dt_start=None
        )
        metrics.total += 1
        try:
            data = json.load(stream)
            result.threat_level = data["threat_level"]
            result.round_start_budget = data["round_start_budget"]
            result.mid_round_budget = data["mid_round_budget"]
            result.shown_threat = data["shown_threat"]

            metrics.parsed += 1
            yield Dynamic, asdict(result)
        except json.decoder.JSONDecodeError as exc:
            metrics.failed += 1
            LOG.error("Failed to parse json: %s:%s", metrics.archive, metrics.logfile)



def dict_combine_skip_none(a, b):
    result = dict(a)
    for k, v in b.items():
        if v is not None:
            result[k] = v
    return result


class DynamicCombinedParser(BaseParser):

    log_filename = "__none__"

    txt_parser = DynamicTxtParser()
    json_parser = DynamicJsonParser()
    
    def parse_archive(self, directory, archive_filename):
        metrics = MetricsStruct(
            archive=archive_filename,
            logfile="dynamic-combined.meta",
        )

        dynamic_txt_result = None
        dynamic_json_result = None
        for record in self.json_parser.parse_archive(directory, archive_filename):
            if record[0] == Dynamic:
                dynamic_json_result = record[1]
            else:
                yield record
        for record in self.txt_parser.parse_archive(directory, archive_filename):
            if record[0] == Dynamic:
                dynamic_txt_result = record[1]
            else:
                yield record
        if dynamic_json_result and dynamic_txt_result:
            combined_result = dict_combine_skip_none(dynamic_json_result, dynamic_txt_result)
        else:
            combined_result = dynamic_json_result or dynamic_txt_result

        metrics.total += 1
        if combined_result is not None:
            metrics.parsed += 1
            yield Dynamic, combined_result
        else:
            metrics.failed += 1
        yield Metrics, asdict(metrics)
