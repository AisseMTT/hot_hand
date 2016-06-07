from bs4 import BeautifulSoup
from selenium import webdriver
import pprint
import urllib
import re
import csv
import pdb

player_id = '2546'
URL = 'http://stats.nba.com/player/#!/' + player_id

class Player_info():
	def __init__(self, player_id):
		self.player_id = player_id
		self.base_url = 'http://stats.nba.com/player/#!/'
		self.age = None
		self.player_number = None
		self.years_in_league = None
		self.height = None
		self.weight = None
		self.position = None
		self.url = self.base_url + self.player_id
		self.soup = self.urlToSoup(self.url, selenium = True)

	def set_player_data(self):
		"""
		Set player data fields
		"""
		self.age = self.get_player_age(self.soup)
		self.years_in_league = self.get_player_years_in_league(self.soup)
		self.height = self.get_player_height(self.soup)
		self.weight = self.get_player_weight(self.soup)
		self.position = self.get_player_position(self.soup)
		self.player_number = self.get_player_number(self.soup)

	def output_to_dict(self):
		data = {
			"player_id" : self.player_id,
			"url" : self.base_url,
			"age" : self.age,
			"years_in_league" : self.years_in_league,
			"height" : self.height,
			"weight" : self.weight,
			"position" : self.position,
			"player_number" : self.player_number
		}
		return data

	def pretty_print(self):
		"""
		Pretty internals
		"""
		pp = pprint.PrettyPrinter(indent = 4)
		pp.pprint(self.output_to_dict())

	def urlToSoup(self, url, selenium = False):
	    """
	    Given a url return soup object
	    set `selenium` to True if we need web driver
	    to load dynamic content...
	    """
	    if selenium:
	        browser = webdriver.Firefox()
	        browser.get(url)
	        soup = BeautifulSoup(browser.page_source, "html.parser")
	        browser.close()
	    else:
	        htmlData = urllib.urlopen(url).read()
	        soup = BeautifulSoup(htmlData, "html.parser")
	    
	    return soup


	def get_player_age(self, soup):
		"""
		Return player age int
		"""
		targets = soup.find_all("div", class_ = "ng-binding")
		if len(targets) < 4: return None

		age_blob = targets[3].get_text()
		pattern = 'Age:\s([1-4][0-9]),'
		age = re.findall(pattern, age_blob)

		if not age: return None
		age = int(age[0])
		return age

	def get_player_years_in_league(self, soup):
		"""
		Return player years in leauge (int)
		"""
		if not self.soup: return None

		targets = soup.find_all("div", class_ = "ng-binding ng-scope")
		if len(targets) < 1: return None

		experience_blob = targets[0].get_text()
		pattern = 'Exp:\s([1-9][0-9]?) years'
		years = re.findall(pattern, experience_blob)

		if not years: return None
		years = int(years[0])
		return years

	def get_player_number(self, soup):
		"""
		Return player years in leauge (int)
		"""
		targets = soup.find_all("div", class_ = "ng-binding")
		if len(targets) >= 2:
			return targets[1].get_text()
		return None

	def get_player_weight_and_height(self, soup):
		"""
		Notes
		"""
		targets = soup.find_all("div", class_ = "ng-binding")
		if len(targets) < 3: return None
		
		wh_blob = targets[2].get_text()
		return wh_blob

	def get_player_height(self, soup):
		"""
		Notes
		"""
		wh_blob = self.get_player_weight_and_height(soup)
		if not wh_blob: return None

		pattern = '([5-7])-([0-9][0-2]?)'
		height = re.findall(pattern, wh_blob)

		if not height: return None
		h_feet = int(height[0][0])
		h_inches = int(height[0][1])
		return h_feet * 12 + h_inches

	def get_player_weight(self, soup):
		"""
		Notes
		"""
		wh_blob = self.get_player_weight_and_height(soup)
		if not wh_blob: return None

		pattern = '([1-3][0-9]{2})'
		weight = re.findall(pattern, wh_blob)

		if not weight: return None
		return int(weight[0])


	def get_player_position(self, soup):
		"""
		Notes
		"""
		targets = soup.find_all("span", class_ = "ng-binding")
		
		if not targets: return None
		position = targets[0].get_text()
		return position


# def createUserCSV(players_data, filePath):
#     """
#     Given a list of recommendation objects, write to a csv file
#     """
#     if len(players_data) > 0:
#         keys = palyers_data[0].keys()
#         with open(filePath + 'players_info.csv', 'wb') as output_file:
#             dict_writer = csv.DictWriter(output_file, keys)
#             dict_writer.writeheader()
#             dict_writer.writerows(players_data)

if __name__ == '__main__':
	player_data_path = 'player_info/'
	### Read in ids
	### -----------
	ids = []
	with open('good_ids.csv', 'r') as input:
	    reader = csv.reader(input, delimiter = ',')
	    next(reader, None) ## skip header
	    for row in reader:
	      ids.append(row[1])

	ids = ['101107', '']

	players_data = []
	for id in ids:
		player = Player_info(id)
		player.set_player_data()
		players_data.append(player.output_to_dict())

	keys = players_data[0].keys()
	with open(player_data_path + 'players_info.csv', 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(players_data)


# soup = urlToSoup(url, selenium = True)
# print get_player_years_in_league(soup)
# print get_player_height(soup)


