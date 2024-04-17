from scripts.rosters import *
from scripts.fantraxBBR import *

#get user inputs

def concatStats(df):
    dfs={}
    for i in df:
        dfs=pd.concat([df[i] for i in df])
    return dfs

league=input("input league id:")

wk = input("Would you like weekly(input 'week') or Daily data (input 'day'):")

period=input("Which period (just the number):")

loc1=input("Where do you want the batting data:")
loc2=input("Where do you want the pitching data:")

#store the objects of fantrax data
leagueData=fantraxBBR(league,period,periodType=wk)

#place batting data in location specified
print(f"Saving Batting CSV to {loc1}")
#get batting stats
bstats=leagueData.linkBatting()
#concat batting stats
bstatsfull=concatStats(bstats)
#save to a csv of user choice
bstatsfull.to_csv(f"{loc1}raw_active_batting_stats.csv")
print(f"Batting CSV saved to {loc1}")


#place pitching data in location specified
print(f"Saving Pitching CSV to {loc1}")
#get pitching stats
pstats=leagueData.linkPitching()
#concat pitching stats
pstatsfull=concatStats(pstats)
#save to a csv of user choice
pstatsfull.to_csv(f"{loc1}raw_active_pitching_stats.csv")
print(f"Pitching CSV saved to {loc1}")

#done
print("Done!")





