import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

"""
Scrape dota2 wiki for hero attributes, and wrangle into pandas dataframe for
future use
"""
def getHeroDataframe():
	url = 'https://dota2.gamepedia.com/Table_of_hero_attributes'
	# Located by finding on dota2 wiki
	table_c_name = "evenrowsgray wikitable sortable"
	request_text = requests.get(url).text
	soup = BeautifulSoup(request_text,'lxml')
	hero_table = soup.find('table',{'class':table_c_name})
	heros = hero_table.findAll('tr')
	clean = re.compile('<.*?>')
	table_label_section = heros[0]


	colNames = []

	for section in table_label_section.findAll('th'):
		shortCode = section.text.strip()

		possTitle = section.find('span')
		description = ""
		if possTitle:
			description = possTitle.get('title')
		
		colNames.append(shortCode)

	hero_list = []

	for hero in heros[1:]:
		curr_hero = []
		for section in hero.findAll('td'):
			attr = section.text.strip()

			# Special case for primary attribute
			if not attr:
				attr = section.find('a').get('title')

			curr_hero.append(attr)

		hero_list.append(curr_hero)


	df = pd.DataFrame(hero_list, columns = colNames ) 

	return df


hero_df = getHeroDataframe()
hero_df.to_csv('hero_stats.csv', index = False)
