WITH nmap as (
--Some guys show up from the pmap.. but others arent confrimed so 
--we gotta try and build out a name based search function
--even though this goes against everything in databasing 
--i'm gonna do it anyway because I cant find a reliably upated source
SELECT 
SUBSTRING(FANTRAXID,2,LEN(FANTRAXID)-2) as fanid
,MLBID AS mlbid
from pmap)

,stage1 AS (
    SELECT *, split(name,' ') as new_name FROM stats 
)
,stage2 AS (
    SELECT * ,new_name[2] || ', ' || new_name[1] as mapName FROM stage1 
)
,stage3 AS ( 
    SELECT a.*, p.fanid, if(p.fanid is null,1,0) as mapFlag FROM stage2 a
    left join nmap p 
    on a.mlbid = p.mlbid
)

SELECT 
f.team_name
,f.id 
,f.position
,f.name as fantrax_name
,s.*
FROM fantrax f 
LEFT JOIN stage3 s
ON if(s.mapFlag = 1,f.name COLLATE NOCASE.NOACCENT,f.id) = if(s.mapFlag = 1,s.mapName,s.fanid)
--on f.id = s.fanid