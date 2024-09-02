select
  week_start,
  sum(players) as players
from (

    select
    date(dt_start, 'weekday 1') as week_start,
    --   x.round_id,
    --   server,
    players
    from (
        select
        round_id,
        count(*) as players,
        min(dt) as dt_start
        from manifest
        group by round_id
    ) as x
    left join
    round_archive_url as y
    on (x.round_id == y.round_id)
    where server == 'terry'
)
group by week_start
order by week_start;