select
  ckey,
  server,
  count(*) as rounds,
  sum(lines) as total_lines,
  sum(characters) as total_characters,  
  avg(lines) as avg_lines,
  avg(characters) as avg_characters
from (
    select
      game.round_id as round_id,
      lower(ckey) as ckey,
      server,
      count(*) as lines,
      sum(length(text)) as characters
    from game as game
    left join round_archive_url as url on (game.round_id = url.round_id)
    where category = 'GAME-SAY'
      and ckey is not null
      and reason is null
      and forced is null
    group by game.round_id, lower(ckey)
)
group by server, ckey
having rounds > 30
order by avg_characters desc
;