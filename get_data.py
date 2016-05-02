import time
import urllib
import requests
import json
import pdb
import re
import goldsberry
import pandas as pd
import numpy as np
import csv
import random
from selenium import webdriver
from bs4 import BeautifulSoup
print goldsberry.__version__

player_data_path = 'player_data/'
player_id = '203500'

### Read in ids
### -----------
ids = []
with open('player_ids.csv', 'r') as input:
  reader = csv.reader(input, delimiter = ',')
  for row in reader:
    ids.append(row[0])

#####
##### get_player_shot_data()
##### ----------------------
##### Arg    :: player id string
##### Return :: all shot data for player_id from 2014-2015 season
#####
def get_player_shot_data(player_id):
  
  ## URL
  url = 'http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=' +\
      '00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=' +\
      '&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2014-15&AheadBehind=&PlayerID=' + player_id +\
      '&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=' +\
      'Regular+Season&SeasonSegment=&GameID='
  # url = 'http://stats.nba.com/stats/playerdashptshotlog?'+ \
  #   'DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&' + \
  #   'Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&' + \
  #   'PlayerID='+player_id+'&Season=2014-15&SeasonSegment=&' + \
  #   'SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision='
  
  ## Use selenium
  browser = webdriver.Firefox()
  browser.get(url)
  soup = BeautifulSoup(browser.page_source, "html.parser")
  browser.close()
  html_str = str(soup)

  ## Extract JSON
  front_pattern = '(<html xmlns=.+<pre>)'
  rear_pattern = '</pre></body></html>'
  html_str = re.sub(front_pattern, '', html_str)
  html_str = re.sub(rear_pattern, '', html_str)
  
  ## Data saved to JSON
  player_data = json.loads(html_str)
  return player_data

#####
##### make_shots_df()
##### ---------------
##### Arg    :: player json data (from get_player_shot_data())
##### Return :: shots in pandas data.frame
#####
def make_shots_df(player_json):
  headers = player_json['resultSets'][0]['headers']
  shots = player_json['resultSets'][0]['rowSet']
  shot_df = pd.DataFrame(shots, columns = headers)
  return shot_df

#####
##### player_data_to_csv()
##### ---------------
##### Args   :: player id, shots data frame, file path
#####
def player_data_to_csv(player_id, shots_df, path):
  shots_df.to_csv(path + player_id + '.csv')

player_json = get_player_shot_data(player_id)
print player_json
shot_df = make_shots_df(player_json)
player_data_to_csv(player_id, shot_df, player_data_path)

# player_data = get_player_shot_data('201167')
# headers = player_data['resultSets'][0]['headers']
# shots = player_data['resultSets'][0]['rowSet']
# shot_df = pd.DataFrame(shots, columns=headers)
# print shot_df.head()




# code from
# http://www.danielforsyth.me/exploring_nba_data_in_python/

# teams ={'wizards':{  
#                    'garrett temple':'202066',
#                    'andre miller':'1889',
#                    'kevin seraphin':'202338',
#                    'otto porter':'203490',
#                    'rasual butler':'2446',
#                    'kris humphries':'2743',
#                    'nene hilario':'2403',
#                    'paul pierce':'1718',
#                    'marcin gortat':'101162',
#                    'bradley beal':'203078',
#                    'john wall':'202322'
#                    }}

# players = []  
# player_stats = {'name':None,'avg_dribbles':None,'avg_touch_time':None,'avg_shot_distance':None,'avg_defender_distance':None}

# def find_stats(name,player_id):  
#     #NBA Stats API using selected player ID
#     url = 'http://stats.nba.com/stats/playerdashptshotlog?'+ \
#     'DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&' + \
#     'Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&' + \
#     'PlayerID='+player_id+'&Season=2014-15&SeasonSegment=&' + \
#     'SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision='

#     #Create Dict based on JSON response
#     pdb.set_trace()
#     response = requests.get(url)
#     shots = response.json()['resultSets'][0]['rowSet']
#     data = json.loads(response.text)

#     #Create df from data and find averages 
#     headers = data['resultSets'][0]['headers']
#     shot_data = data['resultSets'][0]['rowSet']
#     df = pd.DataFrame(shot_data,columns=headers) 
#     avg_def = df['CLOSE_DEF_DIST'].mean(axis=1)
#     avg_dribbles = df['DRIBBLES'].mean(axis=1)
#     avg_shot_distance = df['SHOT_DIST'].mean(axis=1)
#     avg_touch_time = df['TOUCH_TIME'].mean(axis=1)

#     #add Averages to dictionary then to list
#     player_stats['name'] = name
#     player_stats['avg_defender_distance']=avg_def
#     player_stats['avg_shot_distance'] = avg_shot_distance
#     player_stats['avg_touch_time'] = avg_touch_time
#     player_stats['avg_dribbles'] = avg_dribbles
#     players.append(player_stats.copy())

# for x in teams:  
# 	for y in teams[x]:
# 		find_stats(y,teams[x][y])

# cols = ['name','avg_defender_distance','avg_dribbles','avg_shot_distance','avg_touch_time']  
# df = pd.DataFrame(players,columns = cols)  

# print df.head()
