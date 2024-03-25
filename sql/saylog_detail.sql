select
  *
from game_say
where lower(ckey) = ""
  and ckey is not null
  and reason is null
  and forced is null
order by round_id, dt;