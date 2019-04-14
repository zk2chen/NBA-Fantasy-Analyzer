# %matplotlib inline
from selenium import webdriver
from pandas import *
import pandas
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import *

path_to_chromedriver = r'C:\Users\zhika\Miniconda3\pkgs\chromedriver-2.35-0\Library\bin\chromedriver' # Path to access a chrome driver
browser = webdriver.Chrome(executable_path=path_to_chromedriver)

url = 'https://stats.nba.com/leaders/?Season=2018-19&SeasonType=Regular%20Season'
browser.get(url)

browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]').click()

table = browser.find_element_by_class_name('nba-stat-table__overflow')

player_ids = []
player_names = []
player_stats = []

for line_id, lines in enumerate(table.text.split('\n')):
    if line_id == 0:
        column_names = lines.split(' ')[1:]
    else:
        if line_id % 3 == 1:
            player_ids.append(lines)
        if line_id % 3 == 2:
            player_names.append(lines)
        if line_id % 3 == 0:
            player_stats.append( [float(i) for i in lines.split(' ')] )

db = pandas.DataFrame({'player': player_names,
                       'GP': [i[0] for i in player_stats],
                       'MIN': [i[1] for i in player_stats],
                       'PTS': [i[2] for i in player_stats],
                       'FGM': [i[3] for i in player_stats], 
                       'FGA': [i[4] for i in player_stats],
                       '3PM': [i[6] for i in player_stats],
                       '3PA': [i[7] for i in player_stats],
                       'FTM': [i[9] for i in player_stats],
                       'FTA': [i[10] for i in player_stats],
                       'REB': [i[14] for i in player_stats],
                       'AST': [i[15] for i in player_stats],
                       'STL': [i[16] for i in player_stats],
                       'BLK': [i[17] for i in player_stats],
                       'TOV': [i[18] for i in player_stats],
                       }
                     )

db = db[['player', 
         'GP', 
         'MIN', 
         'PTS', 
         'FGM', 
         'FGA',  
         '3PM', 
         '3PA', 
         'FTM',
         'FTA', 
         'REB',
         'AST',
         'STL',
         'BLK',
         'TOV']
      ]

db.to_pickle('18-19-nba_stats.pkl')
