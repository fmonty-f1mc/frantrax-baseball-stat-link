import requests
import pandas as pd
#import json
#import pybaseball
#import duckdb

#base url from fantrax api just easy to put here
baseUrl="https://www.fantrax.com/fxea/general/"

class fantraxRosters:

    def __init__(self,leagueID,period=1):
        self.leagueID=leagueID
        self.period=period
        rosters=[]
        team=requests.get(f"{baseUrl}getLeagueInfo?leagueId={leagueID}").json()['teamInfo']
        #once requested we'll just put this into a json format to display out and create easy manipulation for later
        for i in team:
            rosters.append(team[i])
        self.rosters=rosters

        #get a blank dict to add in the player rosters
        playerRosters={}
        #get player data by rosters 
        base=requests.get(baseUrl+f"getTeamRosters?leagueId={self.leagueID}&period={period}").json()["rosters"]
        for i in self.rosters:
            #lets turn this into a pandas dataframe for easy use later
            playerRosters[i["name"]]=pd.DataFrame(base[i["id"]]['rosterItems'])
        #spit this out for use later
        self.playerRosters=playerRosters
        

    def getID(self,teamName):
        #wanted an easy way to get the id from just the name available
        #want to add a regex search function later on.. but that's future
        for i in self.rosters:
            if teamName.lower() in i["name"].lower():
                teamID=i["id"]

        try:
            teamID 
        except:
            return "Team Name Not in Roster"
        else:
            return teamID
