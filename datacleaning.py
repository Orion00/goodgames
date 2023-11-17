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
import urllib.parse
import time
# %%
games = pd.read_csv("init_data.csv")
#games = games[295:301]

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
        #params['exact'] = 0
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
    time.sleep(1)

games['game_id'] = game_id
games
# %%
games.to_csv("partial_data.csv",index=False)

### Mechanics
# %%
games = pd.read_csv("partial_data.csv")
gam = games.copy(deep=True)
gam = gam[gam['game_id'].notnull()]
gam = gam[0:25]
gam
# %%
game_id = [str(int(i)) for i in gam['game_id']]
game_id

# %%
a_url = "https://boardgamegeek.com/xmlapi/boardgame/"
batch_size = 25
num_batches = len(game_id) // batch_size + (1 if len(game_id) % batch_size > 0 else 0)


for batch_num in range(num_batches):
    start_idx = batch_num * batch_size
    end_idx = min((batch_num + 1) * batch_size, len(game_id))
    current_batch = game_id[start_idx:end_idx]

    id_string = ",".join(current_batch)

    print("Batch",batch_num)
    if(batch_num > 1):
        print(id_string)
    full_url = a_url + id_string
    r = requests.get(full_url)
    bgg_dict = xmltodict.parse(r.content)

    min_players = []
    max_players = []
    playing_time = []
    mechanics = []

    for game in bgg_dict['boardgames']['boardgame']:
        min_players.append(game['minplayers'])
        max_players.append(game['maxplayers'])
        playing_time.append(game['playingtime'])
        mechanics.append([m['#text'] for m in game['boardgamemechanic']])
    time.sleep(5)
    


gam['min_players'] = min_players
gam['max_players'] = max_players
gam['playing_time_min'] = playing_time
gam['mechanics'] = mechanics
# %%
mechanics_encoded = pd.get_dummies(gam['mechanics'].apply(pd.Series).stack()).sum(level=0)
gam = pd.concat([gam, mechanics_encoded], axis=1)
gam
# %%
gam.to_csv("full_data.csv",index=False)