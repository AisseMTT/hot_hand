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


##########
##########
########## Helpers
##########
##########
def get_player_shot_data(player_id):
  """
  get_player_shot_data()
  ----------------------
  Arg    :: player id string
  Return :: all shot data for player_id from 2014-2015 season
  """
  
  ## URL
  url = 'http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=' +\
      '00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=' +\
      '&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2014-15&AheadBehind=&PlayerID=' + player_id +\
      '&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=' +\
      'Regular+Season&SeasonSegment=&GameID='
  
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

def make_shots_df(player_json):
  """
  make_shots_df()
  ---------------
  Arg    :: player json data (from get_player_shot_data())
  Return :: shots in pandas data.frame
  """
  headers = player_json['resultSets'][0]['headers']
  shots = player_json['resultSets'][0]['rowSet']
  shot_df = pd.DataFrame(shots, columns = headers)
  return shot_df

def player_data_to_csv(player_id, shots_df, path):
  """
  player_data_to_csv()
  --------------------
  Args   :: player id, shots data frame, file path
  """
  shots_df.to_csv(path + player_id + '.csv')



##########
##########
########## Main
##########
##########
if __name__ == '__main__':
  player_data_path = 'player_data/'
  
  already_gathered_ids  = []
  with open('good_ids.csv', 'r') as input:
    reader = csv.reader(input, delimiter = ',')
    next(reader, None) ## skip header
    for row in reader:
      already_gathered_ids.append(row[1])

  ### Read in ids
  ### -----------
  ids = []
  with open('player_ids.csv', 'r') as input:
    reader = csv.reader(input, delimiter = ',')
    for row in reader:
      ids.append(row[0])

  for player_id in ids:
    if player_id in already_gathered_ids:
      print "already seen: ", player_id
      continue
    player_json = get_player_shot_data(player_id)
    shot_df = make_shots_df(player_json)
    player_data_to_csv(player_id, shot_df, player_data_path)

## Sample get data for an individual player
# player_json = get_player_shot_data(player_id)
# shot_df = make_shots_df(player_json)
# player_data_to_csv(player_id, shot_df, player_data_path)

## keep for checking urls
# http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2014-15&AheadBehind=&PlayerID=203112&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=Regular+Season&SeasonSegment=&GameID=



