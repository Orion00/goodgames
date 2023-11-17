### Beefing up Data
# Grab game_id, then mechanics for each game

# Uses scraping and API from boardgamegeek.com.
# Documentation is found at https://boardgamegeek.com/wiki/page/BGG_XML_API&redirectedfrom=XML_API#
# and https://api.geekdo.com/xmlapi2
# Terms of Use are here https://boardgamegeek.com/wiki/page/XML_API_Terms_of_Use

### Delays
# Request is done for each row in the dataset, so 500 calls total
DELAY_FOR_IDS = 1

# Requests are done in batches of 25. 500 / 25 = 20, so 20 calls total
DELAY_FOR_MECHANICS = 5

# %%
import pandas as pd
import numpy as np
import xmltodict
import requests
import urllib.parse
import time
# %%
games = pd.read_csv("data/init_data.csv")

### Add game_ids
# %%
a_url = "https://boardgamegeek.com/xmlapi/"

def checkIf(obj,data_type):
    return type(obj) == data_type

game_id = []
for index,row in games.iterrows():
    base_url = "https://boardgamegeek.com/xmlapi/search"
    game_name = str(row['title'])
    params = {'search': game_name, 'exact':1}

    # Check for hyphen instead of hyphen minus character
    if "–" in game_name:
        new_game_name = game_name.replace(" – ", " ")
        new_game_name = urllib.parse.quote(new_game_name, safe='')
        params = {}
        base_url = "https://boardgamegeek.com/xmlapi/search?search="+new_game_name
    
    response = requests.get(base_url, params=params)
    bgg_dict = xmltodict.parse(response.content)
    this_id = np.NaN
    if (len(bgg_dict['boardgames']) == 1):
        print("Didn't find the game:",game_name,"(rank "+str(row['rank'])+")")
        print(response.url)
        game_id.append(this_id)
        continue
    if (checkIf(bgg_dict['boardgames']['boardgame'],list)):
        for game_returned in bgg_dict['boardgames']['boardgame']:
            if (checkIf(game_returned['name'],dict)):
                if (game_returned['name']['#text'] == game_name):
                    if 'yearpublished' in game_returned:
                        this_year = game_returned['yearpublished']
                        if this_year == str(row['year']):
                            this_id = game_returned['@objectid']
                            break
                        else:
                            #print("Dup with wrong year")
                            pass
                    else:
                        print("Found dup with no year")
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
        if (checkIf(game_returned['name'],dict)):
            if (game_returned['name']['#text'] == game_name):
                this_id = game_returned['@objectid']
        elif checkIf(game_returned['name'],str):
            if (game_returned['name'] == game_name):
                this_id = game_returned['@objectid']
        else:
            print("Something is very wrong")
            print()
    game_id.append(this_id)
    time.sleep(DELAY_FOR_IDS)

games['game_id'] = game_id
games
# %%
games.to_csv("data/partial_data.csv",index=False)

### Add Mechanics
# %%
games = pd.read_csv("data/partial_data.csv")
games = games[games['game_id'].notnull()]
games
# %%
game_id = [str(int(i)) for i in games['game_id']]

# %%
a_url = "https://boardgamegeek.com/xmlapi/boardgame/"
batch_size = 25
num_batches = len(game_id) // batch_size + (1 if len(game_id) % batch_size > 0 else 0)

min_players = []
max_players = []
playing_time = []
mechanics = []

for batch_num in range(num_batches):
    start_idx = batch_num * batch_size
    end_idx = min((batch_num + 1) * batch_size, len(game_id))
    current_batch = game_id[start_idx:end_idx]

    id_string = ",".join(current_batch)

    full_url = a_url + id_string
    r = requests.get(full_url)
    bgg_dict = xmltodict.parse(r.content)

    for game in bgg_dict['boardgames']['boardgame']:
        min_players.append(game['minplayers'])
        max_players.append(game['maxplayers'])
        playing_time.append(game['playingtime'])
        if 'boardgamemechanic' not in game:
            print("No mechanics")
            mechanics.append([])
        else:
            if checkIf(game['boardgamemechanic'],list):
                mechanics.append([m['#text'] for m in game['boardgamemechanic']])
            else:
                mechanics.append(game['boardgamemechanic']['#text'])
    time.sleep(DELAY_FOR_MECHANICS)
    


games['min_players'] = min_players
games['max_players'] = max_players
games['playing_time_min'] = playing_time
games['mechanics'] = mechanics
# %%
mechanics_encoded = pd.get_dummies(games['mechanics'].apply(pd.Series).stack()).sum(level=0)
games = pd.concat([games, mechanics_encoded], axis=1)
games
# %%
games.to_csv("data/full_data.csv",index=False)
