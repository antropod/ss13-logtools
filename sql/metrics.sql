select *
from metrics
where logfile <> 'cargo.html'
 and (total = 0 or failed);