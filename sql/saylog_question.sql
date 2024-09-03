select
  ckey,
  text,
  count(*) as lines
from game
where category = 'GAME-SAY'
  and text = '?'
  and ckey is not null
  and reason is null
  and forced is null
group by ckey
order by lines desc;