select
  machine,
  count(round_id) as rounds,

  round(sum(iron), 2) as iron,
  round(avg(iron), 2) as iron_avg,
  
  round(sum(glass), 2) as glass,
  round(avg(glass), 2) as glass_avg,
  
  round(sum(plasma), 2) as plasma,
  round(avg(plasma), 2) as plasma_avg,
  
  round(sum(gold), 2) as gold,
  round(avg(gold), 2) as gold_avg,
  
  round(sum(silver), 2) as silver,
  round(avg(silver), 2) as silver_avg,
  
  round(sum(titanium), 2) as titanium,
  round(avg(titanium), 2) as titanium_avg,
  
  round(sum(uranium), 2) as uranium,
  round(avg(uranium), 2) as uranium_avg,

  round(sum(bluespace_crystal), 2) as bluespace_crystal,
  round(avg(bluespace_crystal), 2) as bluespace_crystal_avg,

  round(sum(diamond), 2) as diamond,
  round(avg(diamond), 2) as diamond_avg,

  round(sum(plastic), 2) as plastic,
  round(avg(plastic), 2) as plastic_avg,

  round(sum(bananium), 2) as bananium,
  round(avg(bananium), 2) as bananium_avg
from (
    select
    machine,
    round_id,
      1.0 * sum(iron) / 100 as iron,
      1.0 * sum(glass) / 100 as glass,
      1.0 * sum(plasma) / 100 as plasma,
      1.0 * sum(gold) / 100 as gold,
      1.0 * sum(silver) / 100 as silver,
      1.0 * sum(titanium) / 100 as titanium,
      1.0 * sum(uranium) / 100 as uranium,
      1.0 * sum(bluespace_crystal) / 100 as bluespace_crystal,
      1.0 * sum(diamond) / 100 as diamond,
      1.0 * sum(plastic) / 100 as plastic,
      1.0 * sum(bananium) / 100 as bananium
    from silo
    group by
      machine,
      round_id
)
group by
  machine
having
  rounds > 10
order by
  iron desc
