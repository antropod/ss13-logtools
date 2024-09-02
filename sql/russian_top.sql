select
  text,
  count(*) as cnt
from game
where ru
  and ckey is not null
  and reason is null
  and forced is null
group by text
order by cnt desc
limit 100;
