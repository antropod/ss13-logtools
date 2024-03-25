select
  server,
  count(*) as cnt
from round_archive_url
where dt >= "2024-01-01"
group by server;