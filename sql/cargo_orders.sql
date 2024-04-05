select
    `order`,
    count(*) as rounds,
    sum(purchases) as purchases
from (
    select
        round_id,
        `order`,
        count(*) as purchases
    from cargo_order
    group by round_id, `order`
)
group by `order`
order by purchases desc;