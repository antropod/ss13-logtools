
select
   item,
   count(*) as rounds,
   sum(purchases) as purchases
from (
    select
        round_id,
        item,
        count(*) as purchases
    from uplink_log
    group by
        round_id, item
)
group by item
order by rounds desc;

-- select count(distinct round_id)
-- from uplink_log;