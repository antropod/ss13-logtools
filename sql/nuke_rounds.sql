select
  round_id,
  count(*) as cnt
from manifest
where special_role = 'Nuclear Operative'
group by round_id
order by round_id desc;