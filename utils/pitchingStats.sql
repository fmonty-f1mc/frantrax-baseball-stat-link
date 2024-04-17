WITH stage as (SELECT team_name
             --, Name
             ,SUM(BB) AS BB
             ,SUM(W) AS W
             ,SUM(ER*9) AS ER9
             ,SUM(BB+H) AS WH
             ,SUM(IPCONVERTED) AS IP
             ,sum(SO) AS K
             ,SUM(H) AS H
             ,SUM(HR) AS HR
             ,SUM(SV) AS SV
             ,SUM(HLD) AS HLD
             ,SUM(IF(IP >= 6 AND ER <= 3,1,0)) as QS
        FROM pitch
             group by 1)

select team_name
    ,K
    ,ER9 / IP AS ERA
    ,WH / IP AS WHIP 
    ,HR AS HRA
    ,SV 
    ,HLD 
    ,(SV + HLD) AS SVHD
    ,((QS*3) + (W*2)) AS WQS4
    FROM stage