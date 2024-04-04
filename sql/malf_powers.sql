select
    power,
    count(*) as rounds,
    sum(purchases) as purchases
from (
    select
        round_id,
        power,
        count(*) as purchases
    from malf
    group by
        round_id, power
)
group by power
order by rounds desc