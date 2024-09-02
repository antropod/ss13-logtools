select
  server,
  sum(is_russian) as russians,
  count(*) as total,
  100.0 * sum(is_russian) / count(*) as pct_russians
from (
    select
      server,
      ckey,
      count(*) as rounds,
      sum(messages) as messages,
      sum(ru_messages) as ru_messages,
      sum(ru_messages) > 0 as is_russian
    from (
        select
          server,
          lower(ckey) as ckey,
          round_id,
          sum(ru) as ru_messages,
          count(*) as messages
        from game_say as game
        left join round_archive_url as url
        using (round_id)
        where ckey is not null
          and reason is null
          and forced is null
        group by
          server, lower(ckey), round_id
    )
    group by server, ckey
    having rounds > 100
)
group by server;