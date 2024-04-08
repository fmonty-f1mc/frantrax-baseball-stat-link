WITH nmap as (SELECT 
SUBSTRING(FANTRAXID,2,LEN(FANTRAXID)-2) as fanid
,MLBID AS mlbid
from pmap)

SELECT 
f.id 
,f.position
,s.*
FROM fantrax f 
INNER JOIN nmap p
ON f.id = p.fanid 
INNER JOIN stats s
ON p.mlbid = s.mlbid