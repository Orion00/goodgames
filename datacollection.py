# %%
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re

### Initial Data (Top 500 games)
# Yes, this would have been much easier by using pd.read_html,
# but I already wrote this Selenium code so we're going to go with that.

# %%
i_url = "https://boardgamegeek.com/browse/boardgame/page/1?sort=rank&sortdir=asc"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(i_url)

#### OLD CODE DON'T LOSE
# %%
# rank = []
# title = []
# year = []
# BGG_rating = []
# avg_rating = []
# list_price = []
# amazon_price = []

# for page in range(1,6):
#     container = driver.find_element(By.XPATH,'//*[@id="collectionitems"]/tbody')
#     top_games = container.find_elements(By.XPATH,'//*[@id="row_"]')

#     for g in top_games:
#         g_rank = g.find_element(By.CLASS_NAME,'collection_rank')
#         rank.append(int(g_rank.text))
#         g_title = g.find_element(By.CLASS_NAME,'primary')
#         title.append(g_title.text)
#         g_year = g.find_element(By.TAG_NAME,"span")
#         year.append(int(g_year.text.strip("[()]")))
#         g_ratings = g.find_elements(By.TAG_NAME,'td')
#         BGG_rating.append(float(g_ratings[3].text))
#         avg_rating.append(float(g_ratings[4].text))
#         g_prices = g.find_element(By.CLASS_NAME,'collection_shop')
#         prices_text = g_prices.text.split("\n")
#         g_amazon_price = np.NaN
#         g_list_price = np.NaN
#         for p in prices_text:
#             if "List" in p:
#                 g_list_price = float(p.split('$')[1]) 
#         for p in prices_text:
#             if "Amazon" in p:
#                 g_amazon_price = float(p.split('$')[1])
#                 break
#         list_price.append(g_list_price)      
#         amazon_price.append(g_amazon_price)
    
#     # Moves to the next page
#     page_icons = driver.find_element(By.CLASS_NAME,"fr")
#     next_page = page_icons.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div/div[1]/div/div/form/div/div[1]/a[contains(@title,'%s')]"% str(page+1))
#     next_page.click()

# %%
pat = re.compile(r'(\d\d\d\d)')
games = pd.DataFrame()
list_price = []
amazon_price = []
for page in range(1,6):
    container = driver.find_element(By.XPATH,'//*[@id="collectionitems"]/tbody')
    top_games = container.find_elements(By.XPATH,'//*[@id="row_"]')

    i_url = "https://boardgamegeek.com/browse/boardgame/page/"+str(page)
    temp_games = pd.read_html(i_url)[0]
    list_price = []
    amazon_price = []
    year = []


    for g in top_games:
        g_prices = g.find_element(By.CLASS_NAME,'collection_shop')
        prices_text = g_prices.text.split("\n")
        g_amazon_price = np.NaN
        g_list_price = np.NaN
        for p in prices_text:
            if "List" in p:
                g_list_price = float(p.split('$')[1]) 
        for p in prices_text:
            if "Amazon" in p:
                g_amazon_price = float(p.split('$')[1])
                break
        list_price.append(g_list_price)      
        amazon_price.append(g_amazon_price)

        g_year = g.find_element(By.TAG_NAME,"span")
        year.append(int(g_year.text.strip("[()]")))
    
    temp_games["Board Game Rank"] = pd.to_numeric(temp_games["Board Game Rank"],errors="coerce")
    temp_games = temp_games[temp_games["Board Game Rank"].notna()]
    temp_games["Board Game Rank"] = temp_games["Board Game Rank"].convert_dtypes()
    temp_games["Title"] = temp_games["Title"].str.split(pat,expand=True)[0].str.strip(" (")
    temp_games.rename(inplace=True,columns={"Title":"title","Board Game Rank":"rank","Geek Rating":"BGG_rating","Avg Rating":"avg_rating","Shop":"list_price"})
    temp_games.drop(inplace=True,columns=["Thumbnail image","Num Voters"])
    temp_games['BGG_rating'] = temp_games['BGG_rating'].astype(float)
    temp_games['avg_rating'] = temp_games['avg_rating'].astype(float)
    temp_games['list_price'] = temp_games['list_price'].astype(float)

    temp_games['Shop'] = list_price
    temp_games['amazon_price'] = amazon_price
    temp_games['year'] = year

    

    games = pd.concat([games,temp_games])

    # Moves to the next page
    page_icons = driver.find_element(By.CLASS_NAME,"fr")
    next_page = page_icons.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div/div[1]/div/div/form/div/div[1]/a[contains(@title,'%s')]"% str(page+1))
    next_page.click()

games


# %%

# games = pd.DataFrame()
# games["title"] = title
# games["rank"] = rank
# games["year"] = year
# games["BGG_rating"] = BGG_rating
# games["avg_rating"] = avg_rating
# games["list_price"] = list_price
# games["amazon_price"] = amazon_price

# games.sort_values(by="rank")

# %%
games.to_csv("init_dat.csv",index=False)

# %%
driver.quit()

### Beefing up Data (Gathering data about each game)
# Uses scraping and API from boardgamegeek.com.
# Documentation is found at https://boardgamegeek.com/wiki/page/BGG_XML_API&redirectedfrom=XML_API#
# and https://api.geekdo.com/xmlapi2
# Terms of Use are here https://boardgamegeek.com/wiki/page/XML_API_Terms_of_Use
# %%
from xml.etree import ElementTree
import xmltodict
import requests
from urllib.parse import quote
import time
# %%
game = pd.read_csv("init_data.csv")
#games = games[23:30]
game
print(games)
print(game)
# %%
a_url = "https://boardgamegeek.com/xmlapi/"
# game_name = "Brass: Birmingham".replace(" ","+")
def checkIf(obj,data_type):
    return type(obj) == data_type


game_id = []
for index,row in games.iterrows():
    a_url = "https://boardgamegeek.com/xmlapi/"
    #print("testing",quote(row['title']),str(row['year']))
    game_name = str(row['title'])
    game_year = str(row['year'])
    endpoint = "search?search="+quote(game_name)
    a_url += endpoint
    r = requests.get(a_url)
    bgg_dict = xmltodict.parse(r.content)
    #print(bgg_dict)
    #time.sleep(1)
    this_id = ""
    if (checkIf(bgg_dict['boardgames']['boardgame'],list)):
        for game_returned in bgg_dict['boardgames']['boardgame']:
            print(game_returned)
            # print(game_returned['name']['#text'])
            if (checkIf(game_returned['name'],dict)):
                if (game_returned['name']['#text'] == game_name):
                    # if (len(game_returned['yearpublished']) == 0):
                    
                    # if ((game_returned['yearpublished'] == game_year)):
                    #print("Success",game_name)
                    this_id = game_returned['@objectid']
                    break
            elif checkIf(game_returned['name'],str):
                if (game_returned['name'] == game_name):
                    this_id = game_returned['@objectid']
                    break
            else:
                print("Something is very wrong")
                print()
                    
    else:
        print("Not a list")
    game_id.append(this_id)

games['game_id'] = game_id


# %%
# Data Cleaning
bgg_dict['boardgames']['boardgame'][0]
game_id
# %%
games