
select
  week_start as week_start,
  avg(threat_level) as tl_avg,
  count(*) as rounds,
  sum(t10) as t10,
  sum(t20) as t20,
  sum(t30) as t30,
  sum(t40) as t40,
  sum(t50) as t50,
  sum(t60) as t60,
  sum(t70) as t70,
  sum(t80) as t80,
  sum(t90) as t90,
  sum(t99) as t99,
  sum(t100) as t100
from (
    select
      date(dt_start, 'weekday 1') as week_start,
      threat_level,
      (0 < threat_level and threat_level <= 10) as t10,
      (10 < threat_level and threat_level <= 20) as t20,
      (20 < threat_level and threat_level <= 30) as t30,
      (30 < threat_level and threat_level <= 40) as t40,
      (40 < threat_level and threat_level <= 50) as t50,
      (50 < threat_level and threat_level <= 60) as t60,
      (60 < threat_level and threat_level <= 70) as t70,
      (70 < threat_level and threat_level <= 80) as t80,
      (80 < threat_level and threat_level <= 90) as t90,
      (90 < threat_level and threat_level <= 99) as t99,
      (99 < threat_level and threat_level <= 100) as t100
    from dynamic
    where dt_start > '2023-01-01'
      and dt_start not null
      and threat_level > 0
  )
group by week_start;