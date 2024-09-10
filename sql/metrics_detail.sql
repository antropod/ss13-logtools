select *
from metrics
where logfile = 'game.txt' and failed
order by failed desc;