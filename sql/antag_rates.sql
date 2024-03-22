select
    ckey,
    total,
    antag,
    round(100.0 * antag / total, 2) as antag_rate,
    traitor,
    round(100.0 * traitor / total, 2) as traitor_rate,
    bb,
    round(100.0 * bb / total, 2) as bb_rate,
    cultist,
    round(100.0 * cultist / total, 2) as cultist_rate,
    headrev,
    round(100.0 * headrev / total, 2) as headrev_rate,
    heretic,
    round(100.0 * heretic / total, 2) as heretic_rate,
    nukeop,
    round(100.0 * nukeop / total, 2) as nukeop_rate,
    spy,
    round(100.0 * spy / total, 2) as spy_rate,
    wizard,
    round(100.0 * wizard / total, 2) as wizard_rate
from (
    select
        ckey,
        count(*) as total,
        count(special_role) as antag,
        count(distinct special_role) as roles,
        sum(case when special_role == 'Traitor' then 1 else 0 end) as traitor,
        sum(case when special_role == 'Blood Brother' then 1 else 0 end) as bb,
        sum(case when special_role == 'Cultist' then 1 else 0 end) as cultist,
        sum(case when special_role == 'Head Revolutionary' then 1 else 0 end) as headrev,
        sum(case when special_role == 'Heretic' then 1 else 0 end) as heretic,
        sum(case when special_role == 'Nuclear Operative' then 1 else 0 end) as nukeop,
        sum(case when special_role == 'Spy' then 1 else 0 end) as spy,
        sum(case when special_role == 'Wizard' then 1 else 0 end) as wizard,
        round(10000.0 * count(special_role) / count(*)) / 100 as rate
    from manifest
    where latejoin == "ROUNDSTART"
    group by ckey
)
where total > 30
order by total desc;