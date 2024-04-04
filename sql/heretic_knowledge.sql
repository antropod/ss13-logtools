select
    knowledge,
    count(*) as rounds,
    sum(purchases) as purchases
from (
    select
        round_id,
        knowledge,
        count(*) as purchases
    from heretic
    group by
        round_id, knowledge
)
group by knowledge
order by rounds desc