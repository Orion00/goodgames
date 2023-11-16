# Uses scraping and API from boardgamegeek.com.
# Documentation is found at https://boardgamegeek.com/wiki/page/BGG_XML_API&redirectedfrom=XML_API#
# and https://api.geekdo.com/xmlapi2
# Terms of Use are here https://boardgamegeek.com/wiki/page/XML_API_Terms_of_Use
# %%
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Initial Data (Top 500 games)
# %%
i_url = "https://boardgamegeek.com/browse/boardgame/page/1?sort=rank&sortdir=asc"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(i_url)

# %%
rank = []
title = []
year = []
BGG_rating = []
avg_rating = []
list_price = []
amazon_price = []

container = driver.find_element(By.XPATH,'//*[@id="collectionitems"]/tbody')
top_games = container.find_elements(By.XPATH,'//*[@id="row_"]')

for g in top_games:
    # g_rank = g.find_element(By.CLASS_NAME,'collection_rank')
    # rank.append(g_rank.text)
    # g_title = g.find_element(By.CLASS_NAME,'primary')
    # title.append(g_title.text)
    # g_year = g.find_element(By.TAG_NAME,"span")
    # year.append(g_year.text.strip("[()]"))
    # g_ratings = g.find_elements(By.TAG_NAME,'td')
    # BGG_rating.append(g_ratings[3].text)
    # avg_rating.append(g_ratings[4].text)
    g_amazon_price = g.find_element(By.CLASS_NAME,'ulprice')
    print(g_amazon_price.text)
    amazon_price.append(g_amazon_price.text)

# print(title)
# print(rank)
# print(year)
# print(BGG_rating)
# print(avg_rating)

# %%
driver.quit()
# Beefing up Data (Gathering data about each game)


# Data Cleaning