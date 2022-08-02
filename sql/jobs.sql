select
    dt,
    assigned_role,
    sum(hits) as hits,
    count(*) as rounds
from (
    select
        round_id,
        date(min(dt) over (partition by round_id)) as dt,
        assigned_role,
        count(*) as hits
    from
        manifest
    group by
        round_id, assigned_role
)
group by dt, assigned_role;