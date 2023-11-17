### Beefing up Data
# Grab game_id, then mechanics for each game

# Uses scraping and API from boardgamegeek.com.
# Documentation is found at https://boardgamegeek.com/wiki/page/BGG_XML_API&redirectedfrom=XML_API#
# and https://api.geekdo.com/xmlapi2
# Terms of Use are here https://boardgamegeek.com/wiki/page/XML_API_Terms_of_Use
# %%
import pandas as pd
import numpy as np
import xmltodict
import requests
from urllib.parse import quote
import time
# %%
games = pd.read_csv("init_data.csv")
games = games[295:300]

# %%
a_url = "https://boardgamegeek.com/xmlapi/"

def checkIf(obj,data_type):
    return type(obj) == data_type


game_id = []
for index,row in games.iterrows():
    a_url = "https://boardgamegeek.com/xmlapi/"
    #print("testing",quote(row['title']),str(row['year']))
    game_name = str(row['title'])
    game_year = str(row['year'])
    endpoint = "search?search="+quote(game_name)

    # params = {'search': game_name}
    # r = requests.get(a_url+"search/", params=params)
    # print(r.content)

    a_url += endpoint
    r = requests.get(a_url)
    bgg_dict = xmltodict.parse(r.content)
    print(bgg_dict)
    #time.sleep(1)
    this_id = np.NaN
    if (checkIf(bgg_dict['boardgames']['boardgame'],list)):
        for game_returned in bgg_dict['boardgames']['boardgame']:
            #print(game_returned)
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
        game_returned = bgg_dict['boardgames']['boardgame']
        #print(game_returned)
        # print(game_returned['name']['#text'])
        if (checkIf(game_returned['name'],dict)):
            if (game_returned['name']['#text'] == game_name):
                # if (len(game_returned['yearpublished']) == 0):
                
                # if ((game_returned['yearpublished'] == game_year)):
                #print("Success",game_name)
                this_id = game_returned['@objectid']
        elif checkIf(game_returned['name'],str):
            if (game_returned['name'] == game_name):
                this_id = game_returned['@objectid']
        else:
            print("Something is very wrong")
            print()
    game_id.append(this_id)

games['game_id'] = game_id


games
# %%
games

# %%
a_url = "https://boardgamegeek.com/xmlapi/"

game_id_1 = game_id[0:50]


endpoint = "boardgame/="+quote(game_name)
a_url += endpoint
r = requests.get(a_url)
bgg_dict = xmltodict.parse(r.content)

# %%
# r = requests.get(a_url)
a_url