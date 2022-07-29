select
    count(*) as parsed_log_lines,
    count(distinct round_id) as parsed_rounds
from uplink;