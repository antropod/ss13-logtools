select
   item,
   count(*) as rounds,
   sum(purchases) as purchases
from (
    select
        round_id,
        item,
        count(*) as purchases
    from uplink
    where uplink_type = 'nukeops'
    group by
        round_id, item
)
group by item
order by rounds desc;