select
    x.map_name as map_name,
    x.server as server,
    sum(x.rounds) as rounds,
    sum(y.rounds) as total,
    round(100.0 * sum(x.rounds) / sum(y.rounds), 2) as percent
from (
    select
        map_name,
        url.server as server,
        count(*) as rounds
    from mapinfo as map
    left join round_archive_url as url on (map.round_id = url.round_id)
    group by map_name, server
) as x
left join (
    select
        url.server as server,
        count(*) as rounds
    from mapinfo as map
    left join round_archive_url as url on (map.round_id = url.round_id)
    group by server
    order by rounds desc
) as y
on (x.server = y.server)
group by x.server, x.map_name
having x.rounds > 5
order by server, rounds desc
