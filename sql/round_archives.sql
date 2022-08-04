select
    server,
    year,
    count("rounds") as rounds
from (
    select
        server,
        strftime("%d", dt) as day,
        strftime("%m", dt) as month,
        strftime("%Y", dt) as year
    from round_archive_url
)
group by server, year
order by server, year;