select
   server,
   map_name,
   x, y, z,
   count(*) as cnt_messages
from (
    select
      *
    from game
    left join mapinfo using (round_id)
    left join round_archive_url using (round_id)
    where category = 'GAME-SAY'
        and ckey is not null
        and reason is null
        and forced is null
        and map_name is not null
)
where dt > '2024-05-01'
group by server, map_name, x, y, z;