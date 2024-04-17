--add hold flag for pichers that meet the criteria
WITH hld_flg AS (SELECT
     p.*
     ,IF(p.GS = 0 AND p.SV IS NULL AND p.W is null AND p.IP >= 0.1, 1, 0) AS hld_flg
     ,strptime(Date, '%b %d, %Y') as game_date
    FROM initpull p
    WHERE 1=1 )

,game_log_hld AS(
SELECT distinct
     p.team_name
    ,s.game_date
    ,p.mlbID
    ,MIN(fld_score) as pre_fld_score
    ,MAX(post_fld_score) as post_fld_score
    ,MIN(bat_score) as pre_bat_score
    ,max(post_bat_score) post_bat_score
    FROM  hld_flg p
    INNER JOIN stcst s
       ON s.pitcher = p.mlbID
    where 1=1 
    and p.hld_flg = 1
    group by 1,2,3
)

,hlds AS (
    select mlbID 
    ,game_date
    ,1 AS HLD
    from game_log_hld where 1=1 
    and post_bat_score < post_fld_score 
    and pre_bat_score < pre_fld_score
    and (pre_fld_score-pre_bat_score) <= 3 
)

SELECT a.* 
,hlds.HLD 
FROM hld_flg a
LEFT JOIN hlds ON 
a.mlbID = hlds.mlbID
AND a.game_date = hlds.game_date
AND a.hld_flg = 1


