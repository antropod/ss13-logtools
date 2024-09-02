select
    dt,
    count(*) as unique_players,
    sum(total_players) as total_players
from (
    select
        dt,
        ckey,
        count(*) as total_players    
    from (
        select
            date(min(x.dt)) as dt,
            round_id,
            ckey
        from manifest as x
        left join round_archive_url as y
        using (round_id)
        where server == 'terry'
        group by round_id, ckey
    )
    group by dt, ckey
)
group by dt