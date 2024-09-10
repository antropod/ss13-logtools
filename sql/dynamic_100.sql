select
  round_id,
  dt_start,
  threat_level
from dynamic
where threat_level > 99;