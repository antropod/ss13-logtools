select
  logfile,
  sum(total) as total,
  sum(parsed) as parsed,
  100.0 * sum(parsed) / sum(total) as pct_parsed,
  sum(failed) as failed,
  100.0 * sum(failed) / sum(total) as pct_failed,
  sum(skipped) as skipped
from metrics
group by logfile;