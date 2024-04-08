import requests
import pandas as pd
import json
import pybaseball
import duckdb
from scripts.rosters import *
from io import StringIO
import time

#class that just pulls each day you want at one time
class periodBBR:

    def __init__(self,period,period_type='day'):
        #self.leagueid=leagueid
        self.period=period

        ftPeriods=open('utils/fantrax_periods.json')
        self.ftPeriods=json.load(ftPeriods)
        prd=int(period)

        self.periodDates=[x["date_date"] for x in self.ftPeriods if x[f'{period_type}_period'] == prd]

        self.startDate=[x["date_date"] for x in self.ftPeriods if x[f'{period_type}_period'] == prd][0]
        self.endDate=[x["date_date"] for x in self.ftPeriods if x[f'{period_type}_period'] == prd][-1]


    def pitchStats(self):
        df={}
        #so for pitching stats things get tricky.. 
        #For my leauge we use QSs in our categories.. 
        #But BBR doesnt track them.. so I'll need to calc them later.. but need these stats individually

        #need an empty dataframe to store in there for later just in case errors are thrown
        emptybat=duckdb.query("SELECT 'n/a' as id, 'n/a' as position ").to_df()


        #mostly day periods are only 1 date.. but we have exceptions
        for i in self.periodDates:
            time.sleep(30)

            try:
                pybaseball.pitching_stats_range(start_dt=i,end_dt=i)
            except Exception as error:
                print("An exception occurred:", error)
                df[i]=emptybat
            else:
                print("Gathering Pitching Stats...")
                df[i]=pybaseball.pitching_stats_range(start_dt=i,end_dt=i)
        return pd.concat([df[x] for x in df])
                
        
    def batStats(self):
        #we can generally just pull all the stats straight on
        emptybat=duckdb.query("SELECT 'n/a' as id, 'n/a' as position ").to_df()
        #need to address: seems like you cant make too many calls to BBR so I just have a try statment to not throw an error
        try:
            pybaseball.batting_stats_range(start_dt=str(self.startDate), end_dt=str(self.endDate))
        except Exception as error:
            print("An exception occurred:", error)
            return emptybat
        else:
            #use batting stats range to get dayily game summaries
            print("Gathering Batting Stats...")
            stats=pybaseball.batting_stats_range(start_dt=str(self.startDate), end_dt=str(self.endDate))
            if stats.empty:
                print("No Batting stats Found")
                return emptybat
            else:
                print("Batting Stats Gathered!")
                return pybaseball.batting_stats_range(start_dt=str(self.startDate), end_dt=str(self.endDate))



class fantraxBBR:

    def __init__(self,leagueid,period,periodType="week"):

        #############################
        #Need to gather up ID links. 
        #Lucky there are kind people out there on the internet
        #please say thank you to https://www.smartfantasybaseball.com :)


        playerMapLink='1JgczhD5VDQ1EiXqVG-blttZcVwbZd5_Ne_mefUGwJnk'
        r = requests.get(f'https://docs.google.com/spreadsheet/ccc?key={playerMapLink}&output=csv')
        s=str(r.content,'utf-8')
        data = StringIO(s)
        self.playerMap=pd.read_csv(data)

        ################################


        #periods are funny so fantrax uses the term in the app as either week or day based
        #in the api its strictly for days
        #so we can modify that a little bit later, but for now lets just stick to finding stats one day at a time
        #you can borrow my list I created to link period to actual date, but it's possible they are not the same
        #see utils/fantrax_periods.json
        self.period=period
        self.periodType=periodType
        ftPeriods=open('utils/fantrax_periods.json')
        self.ftPeriods=json.load(ftPeriods)
        prd=int(period)

        self.startDate=[x["date_date"] for x in self.ftPeriods if x[f'{periodType}_period'] == prd][0]
        self.endDate=[x["date_date"] for x in self.ftPeriods if x[f'{periodType}_period'] == prd][-1]

        #we'll need to grab fantrax rosters
        #This is gonna get confusing so I'm just gonna keep the rosters name as simply "roster"
        self.rosters=fantraxRosters(leagueid,period).playerRosters

        #within the rosters grab their active players
        #right now we're just gonna worry about the active players for each peroid
        activeRoster={}
        for i in self.rosters:
            activeRoster[i]=self.rosters[i].query("status == 'ACTIVE' ")
        self.activeRoster=activeRoster

            
    def linkPitching(self):
        #empty df for storage
        playerStats={}
        stats=periodBBR(self.period,self.periodType).pitchStats()

        #gonna name player map something simple
        pmap=self.playerMap

        for i in self.activeRoster:

            fantrax=self.activeRoster[i].query("position == 'P' ")
            playerStats[i]=duckdb.query(open('utils/statPull.sql').read()).to_df()
        
        return playerStats
    
    def linkBatting(self):
        #empty df for storage
        playerStats={}
        #i only want to touch BBR once usually, it likes to kick you off
        stats=periodBBR(self.period,self.periodType).batStats()

        #gonna name player map something simple
        pmap=self.playerMap

        for i in self.activeRoster:
            
            fantrax=self.activeRoster[i].query("position != 'P' ")
            playerStats[i]=duckdb.query(open('utils/statPull.sql').read()).to_df()

        return playerStats

        
        