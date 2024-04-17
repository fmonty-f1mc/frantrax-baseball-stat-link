WITH stage as (select team_name
             ,SUM(R) AS R
             ,SUM(H) AS H
             ,SUM(RBI) AS RBI
             ,SUM(HR) AS HR 
             ,SUM(SB) AS SB
             ,SUM(AB) AS AB
             ,SUM(HBP) AS HBP
             ,sum(BB)AS BB
             ,SUM(PA) AS PA
             ,SUM(SH) AS SH
             ,SUM(H - ("2B" + "3B" + HR)) AS "1B"
             ,SUM("2B") as "2B"
             ,SUM("3B") AS "3B"
             from bat GROUP BY 1)
             
             ,stage2 as (
             select team_name
             , SUM(R) AS R
             , SUM(HR) AS HR
             , SUM(RBI) AS RBI
             , sum(SB) AS SB
             , SUM(H/AB) AS BAVG
             , SUM((BB+H+HBP-SH)/PA) AS OBP
             , sum(("1B" + "2B"*2 + "3B"*3 + "HR"*4)/AB) as SLG 
             FROM stage group by 1
             )

             SELECT *, (OBP+SLG) AS OPS FROM stage2

