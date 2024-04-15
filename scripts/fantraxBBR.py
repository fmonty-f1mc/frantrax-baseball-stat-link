import requests
import pandas as pd
import json
import pybaseball
import duckdb
from scripts.rosters import *
from io import StringIO
import time
import re
# coding=utf-8
from unidecode import unidecode
import codecs 

#class that just pulls each day you want at one time
class periodBBR:

    def __init__(self,period):
        #self.leagueid=leagueid
        self.period=period

        ftPeriods=open('utils/fantrax_periods.json')
        self.ftPeriods=json.load(ftPeriods)
        prd=int(period)

        self.periodDates=[x["date_date"] for x in self.ftPeriods if x['day_period'] == prd]

        #self.startDate=[x["date_date"] for x in self.ftPeriods if x[f'{period_type}_period'] == prd][0]
        #self.endDate=[x["date_date"] for x in self.ftPeriods if x[f'{period_type}_period'] == prd][-1]


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
        #return pd.concat([df[x] for x in df])
        return df
                
        
    def batStats(self):
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
                pybaseball.batting_stats_range(start_dt=i,end_dt=i)
            except Exception as error:
                print("An exception occurred:", error)
                df[i]=emptybat
            else:
                print("Gathering Batting Stats...")
                df[i]=pybaseball.batting_stats_range(start_dt=i,end_dt=i)
        #return pd.concat([df[x] for x in df])
        return df



class fantraxBBR:

    def __init__(self,leagueid,period,periodType="week"):

        #############################
        #Need to gather up ID links. 
        #Lucky there are kind people out there on the internet
        #please say thank you to https://www.smartfantasybaseball.com :)

        self.leagueid=leagueid
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

        self.periodDates=[x["date_date"] for x in self.ftPeriods if x[f'{periodType}_period'] == prd]
        self.periods=[x["day_period"] for x in self.ftPeriods if x[f'{periodType}_period'] == prd]

        self.startDate=[x["date_date"] for x in self.ftPeriods if x[f'{periodType}_period'] == prd][0]
        self.endDate=[x["date_date"] for x in self.ftPeriods if x[f'{periodType}_period'] == prd][-1]

        #we'll need to grab fantrax rosters
        #This is gonna get confusing so I'm just gonna keep the rosters name as simply "roster"
        #self.rosters=fantraxRosters(leagueid,period).playerRosters

        #within the rosters grab their active players
        #right now we're just gonna worry about the active players for each peroid
        #activeRoster={}
        #for i in self.rosters:
        #    activeRoster[i]=self.rosters[i].query("status == 'ACTIVE' ")
        #self.activeRoster=activeRoster
        roster={}
        for i in self.periods:
            roster[i]=fantraxRosters(self.leagueid,i)
        self.roster=roster

        #quick lambda function to translate unicode for mostly for those that dont have a connection between mlb and fantrax
        self.uniTranslate=lambda x: unidecode(codecs.escape_decode(x)[0].decode())

    def ipConvert(self,col):
        try:
            int(col)
        except:
            return col
        else:
            dec=int(str(col).split(".")[1])
            num=int(str(col).split(".")[0])

            if dec == 1:
                return num+.33
            elif dec == 2:
                return num+.66
            else:
                return num


            
    def linkPitching(self):
        #empty df for storage
        playerStats={}
        playerStats1={}
        #gonna name player map something simple
        pmap=self.playerMap
        for i in self.periods:            
            dfs=periodBBR(i).pitchStats()
            stats=pd.concat([dfs[x] for x in dfs])
            stats["first_name"]=stats.apply(lambda row: self.uniTranslate(row.Name.split(" ")[0]), axis=1)
            stats["last_name"]=stats.apply(lambda row: self.uniTranslate(row.Name.split(" ")[1]), axis=1)
            stats["IPCONVERTED"]=stats.apply(lambda row: self.ipConvert(row.IP), axis=1)
            for n in self.roster[i].playerRosters:
                fantrax=self.roster[i].playerRosters[n].query("status == 'ACTIVE' ").query("position == 'P' ")
                fantrax["team_name"] = n
                playerStats[str(str(i)+str(n))]=duckdb.query(open('utils/statPull.sql').read()).to_df()
                #playerStats[i]={n:duckdb.query(open('utils/statPull.sql').read()).to_df()}
        
        return playerStats
    
    def linkBatting(self):
        #empty df for storage
        playerStats={}
        playerStats1={}
        #gonna name player map something simple
        pmap=self.playerMap
        for i in self.periods:
            dfs=periodBBR(i).batStats()
            stats=pd.concat([dfs[x] for x in dfs])
            stats["first_name"]=stats.apply(lambda row: self.uniTranslate(row.Name.split(" ")[0]), axis=1)
            stats["last_name"]=stats.apply(lambda row: self.uniTranslate(row.Name.split(" ")[1]), axis=1)
            for n in self.roster[i].playerRosters:
                fantrax=self.roster[i].playerRosters[n].query("status == 'ACTIVE' ").query("position != 'P' ")
                fantrax["team_name"] = n
                playerStats[str(str(i)+str(n))]=duckdb.query(open('utils/statPull.sql').read()).to_df()
                #playerStats[i]={n:duckdb.query(open('utils/statPull.sql').read()).to_df()}
        
        return playerStats

        
        