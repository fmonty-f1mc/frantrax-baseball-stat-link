# frantrax-baseball-stat-link

This repository is for any Fantrax Fantasy Baseball leauges that want to view advanced analytics. 

The classes contained in this repository are specifically designed around my league's purpose. But feel free to branch off and create your own!

I have to give credit to all the online resources I've found that made this possible:
- [pybaseball](https://github.com/jldbc/pybaseball) 
- [Smart Fantasy baseball](https://www.smartfantasybaseball.com)
- [duckDb](https://duckdb.org)

## How to use

I'll try to find time to make this code excecutable so you'll simply run this on your operating system..

But for now, you'll need to install the requirments (available in the requirements.txt) and have the latest python installed.
My installer is pip. 

You can use the classes themselves to your needs, but I've created a simple script fantrax-active-roster-pull.py

Run this and you'll grab all Baseball Reference data from pybaseball (some stat cast data also but I'm trying to limit how much statcast data because I'm afraid of dupes). 

I'll keep this repo updated as the season goes along. So check back for more PRs. 