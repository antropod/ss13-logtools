select
    (select count(*) from game) as game,
    (select count(*) from manifest) as manifest,
    (select count(*) from uplink) as uplink,
    (select count(*) from changeling) as changeling,
    (select count(*) from mapinfo) as mapinfo,
    (select count(*) from uplink) as uplink
;