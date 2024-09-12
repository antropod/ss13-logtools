select
  week_start,
  100.0 * sum(station_destroyed) / count(*) as pct_major,
  100.0 * sum(syndicate_minor) / count(*) as pct_minor,
  100.0 * (sum(syndicate_minor) + sum(station_destroyed)) / count(*) as pct_win,
  sum(station_destroyed) as syndicate_major,
  sum(syndicate_minor) as syndicate_minor,
  sum(syndicate_minor) + sum(station_destroyed) as syndicate_win,
  count(*) as rounds
from (
    select
      round_id,
      date(dt_start, 'weekday 1') as week_start,
      nukeop_result,
      station_integrity,
      station_destroyed,
      (nukeop_result = 'Syndicate Minor Victory!') as syndicate_minor
    from round_end_data
    right join (
        select
          round_id,
          min(dt) as dt_start
        from manifest
        where special_role = 'Nuclear Operative'
         and lower(ckey) = 'livrah'
        group by round_id
    ) nukeop
    using (round_id)
)
group by week_start
order by week_start;