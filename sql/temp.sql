select
  location,
  count(*) as cnt
from game
group by location
order by cnt desc;

select 
  *
from game
where location = 'a'