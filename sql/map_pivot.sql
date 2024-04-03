select
    map_name,
    url.server as server,
    count(*) as rounds
from (
    select
        case
          when map_name in ('MetaStation', 'Delta Station', 'Ice Box Station', 'Birdshot Station', 'Tramstation', 'NorthStar', 'Kilo Station') then map_name
          else 'Other'
        end as map_name,
        round_id
    from mapinfo
) as map

left join round_archive_url as url on (map.round_id = url.round_id)
group by map_name, server
order by rounds desc