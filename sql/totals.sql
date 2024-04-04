select
    (select count(*) from game_say) as game_say,
    (select count(*) from manifest) as manifest,
    (select count(*) from uplink) as uplink,
    (select count(*) from changeling) as changeling,
    (select count(*) from mapinfo) as mapinfo,
    (select count(*) from uplink) as uplink
;