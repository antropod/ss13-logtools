select
    date(strftime('%s', dt) - 86400 * ((strftime('%w', dt) + 6) % 7), 'unixepoch') as dt, -- date to week start
    assigned_role,
    sum(hits) as hits
from (
    select
        dt,
        assigned_role,
        sum(hits) as hits
    from (
        select
            round_id,
            date(min(dt) over (partition by round_id)) as dt,
            assigned_role,
            count(*) as hits
        from
            manifest
        group by
            round_id,
            assigned_role
    )
    group by 
        dt,
        assigned_role
)
group by
    dt,
    assigned_role;