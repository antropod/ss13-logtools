select
  ckey,
  min(round_id) as round_id,
  count(*) rounds
from manifest
group by ckey
order by ckey, round_id;