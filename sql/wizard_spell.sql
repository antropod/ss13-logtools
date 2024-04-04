select
    spell,
    count(*) as rounds,
    sum(purchases) as purchases
from (
    select
        round_id,
        spell,
        count(*) as purchases
    from wizard_spell
    group by
        round_id, spell
)
group by spell
order by rounds desc