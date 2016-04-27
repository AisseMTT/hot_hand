import time
import urllib
import requests
import json
import pdb
import goldsberry
import pandas as pd
import numpy as np
import csv
import random
from selenium import webdriver
from bs4 import BeautifulSoup
print goldsberry.__version__

######
###### Get 2015 player list
######
players = goldsberry.PlayerList()
players2015 = pd.DataFrame(players.players())
# print players2015.head()
id_list = players2015['PERSON_ID']
# ids = [str(id) for id in id_list]


### Write player ids to csv
### ------------------------
# with open('player_ids.csv', 'wb') as output_file:
#   writer = csv.writer(output_file, dialect = 'excel')
#   for id in ids:
#     writer.writerow([id])

### Read in ids
### -----------
ids = []
with open('player_ids.csv', 'r') as input:
  reader = csv.reader(input, delimiter = ',')
  for row in reader:
    ids.append(row[0])

# id_list = ['203500']
def get_shot_data(player_id):
  # print 'sleeping for 5'
  # time.sleep(5)
  # print '==============='
  # print 'player_id: ', player_id
  # print type(player_id)
  # print '==============='
  url = 'http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=' +\
      '00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=' +\
      '&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2014-15&AheadBehind=&PlayerID=' + player_id +\
      '&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=' +\
      'Regular+Season&SeasonSegment=&GameID='
  # print url
  # htmlData = urllib.urlopen(url).read()
  # print htmlData
  # soup = BeautifulSoup(htmlData, "html.parser")
  # print soup
  # data = json.loads(str(soup))
  browser = webdriver.Firefox()
        # browser.set_window_size(1, 1)
  browser.get(url)
  soup = BeautifulSoup(browser.page_source, "html.parser")
  browser.close()
  print soup

  # response = requests.get(url, timeout = 10)
  # return response.status_code

  # print 'response: ', response
  # headers = response.json()['resultSets'][0]['headers']
  # shots = response.json()['resultSets'][0]['rowSet']
  # return shots[0]
# a = ids[:10]
# random.shuffle(a)
# print [get_shot_data(id) for id in a]

print get_shot_data('201167')

# for id in ids:
#   print type(id)
#   curr_shot_data = get_shot_data(id)
#   print curr_shot_data

# player_id = '203919'
# print get_shot_data(player_id)



# url = 'http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=' +\
#       '00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=' +\
#       '&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2014-15&AheadBehind=&PlayerID=' + PlayerID +\
#       '&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=' +\
#       'Regular+Season&SeasonSegment=&GameID='
# Get the webpage containing the data
# response = requests.get(url)
# # # Grab the headers to be used as column headers for our DataFrame
# headers = response.json()['resultSets'][0]['headers']
# # # Grab the shot chart data
# shots = response.json()['resultSets'][0]['rowSet']
# # # data = json.loads(response.text)
# print shots


    
# http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2014-15&AheadBehind=&PlayerID=203112&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=Regular+Season&SeasonSegment=&GameID=
# http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2014-15&AheadBehind=&PlayerID=201935&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=Regular+Season&SeasonSegment=&GameID=







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



# http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=",playerID,"&PlusMinus=N&Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0
# http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=201939&PlusMinus=N&Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0


