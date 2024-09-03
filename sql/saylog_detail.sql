select
  *
from game
where category = 'GAME-SAY'
  and lower(ckey) = ""
  and ckey is not null
  and reason is null
  and forced is null
order by round_id, dt;