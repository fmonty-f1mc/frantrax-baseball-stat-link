SELECT 
 df1.id 
,df1.position 
,df1.status 
,pIDs.name 
,split(pIDs.name,' ')[2] as first_name
,split(pIDs.name,',')[1] as last_name
,pIDs.rotowireId
,pIDs.statsIncId
,pIDs.sportRadarId
FROM df1
LEFT JOIN pIDs
ON df1.id = pIDs.fantraxid