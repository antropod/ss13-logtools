--- TODO: Count Unique players ---

select
   dt,
   sum(new_players) as new_players,
   sum(players) as players
from (
  select
     date(dt_start, 'weekday 1') as dt,
     new_players,
     players
  from (
      select
        round_id,
        min(dt) as dt_start,
        sum(new_player) as new_players,
        count(*) as players
      from (
          select
            dt,
            man.round_id as round_id,
            man.ckey as ckey,
            man.round_id = first_round.round_id as new_player
          from manifest as man
          left join (
            select
              ckey,
              min(round_id) as round_id
            from manifest
            group by ckey
          ) as first_round
          where (man.ckey == first_round.ckey)
      )
      group by round_id
  )
)
group by dt
order by dt