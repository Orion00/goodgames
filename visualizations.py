### Imports
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

games = pd.read_csv("data/full_data.csv")
games_sans_encoding = games.iloc[:,0:11]
games_sans_encoding.describe()


# %%
### Correlation Matrix
sns.heatmap(games_sans_encoding.drop('game_id',axis=1).corr(numeric_only=True))
plt.savefig("visuals/correlationMatrix.png",bbox_inches='tight',pad_inches=.1)

# %%
games_sans_encoding.drop('game_id',axis=1).corr(numeric_only=True)


### Mechanics 
# %%
mechanics_counts_500 = (games.iloc[:,12:].sum(axis=0)).sort_values(ascending=False).head(15)
sns.barplot(y=mechanics_counts_500.index,x=mechanics_counts_500.values,palette="Set2")
plt.ylabel('Mechanics')
plt.xlabel('Frequency')
plt.title('Most Frequent Mechanics in Top 500 Games')
plt.savefig("visuals/mostFreqMechanics500.png",bbox_inches='tight',pad_inches=.1)

# %%
mechanics_counts_100 = (games.head(100).iloc[:,12:].sum(axis=0)).sort_values(ascending=False).head(15)
sns.barplot(y=mechanics_counts_100.index,x=mechanics_counts_100.values,palette="Set2")
plt.ylabel('Mechanics')
plt.xlabel('Frequency')
plt.title('Most Frequent Mechanics in Top 100 Games')
plt.savefig("visuals/mostFreqMechanics100.png",bbox_inches='tight',pad_inches=.1)


# %%
mechanics_counts_50 = (games.head(50).iloc[:,12:].sum(axis=0)).sort_values(ascending=False).head(15)
sns.barplot(y=mechanics_counts_50.index,x=mechanics_counts_50.values,palette="Set2")
plt.ylabel('Mechanics')
plt.xlabel('Frequency')
plt.title('Most Frequent Mechanics in Top 50 Games')
plt.savefig("visuals/mostFreqMechanics50.png",bbox_inches='tight',pad_inches=.1)

#### Subplot Attempt
# %%
# fig, axs = plt.subplots(1,3)
# fig.suptitle('Vertically stacked subplots')
# plt.style.use('fivethirtyeight')
# axs[0].barh(mechanics_counts_500.index, mechanics_counts_500.values)
# axs[1].barh(mechanics_counts_100.index, mechanics_counts_100.values)
# axs[2].barh(mechanics_counts_50.index, mechanics_counts_50.values)


### Rating
# %%
sns.scatterplot(x=games['BGG_rating'],y=games['avg_rating'], hue=games['rank'],palette="flare")
plt.ylabel('Player Rating')
plt.xlabel('BGG Rating')
plt.title('BGG Rating vs Player Rating')

# %%
sns.scatterplot(x=games['amazon_price'],y=games['avg_rating'], hue=games['rank'],palette="flare")
plt.ylabel('Player Rating')
plt.xlabel('Amazon Price')
plt.title('Amazon Price vs Player Rating')
plt.savefig("visuals/mostFreqMechanics50.png",bbox_inches='tight',pad_inches=.1)


# %%
sns.scatterplot(x=games['rank'],y=games['avg_rating'])
sns.scatterplot(x=games['rank'],y=games['BGG_rating'])
plt.legend(["Player Rating","BGG Rating"])
plt.ylabel('Rating')
plt.xlabel('Rank')
plt.title('Rank vs Ratings')
plt.savefig("visuals/rankvsRating.png",bbox_inches='tight',pad_inches=.1)


 # %%
sns.scatterplot(x=games['rank'],y=games['avg_rating'], hue=games['amazon_price'],palette="flare")
plt.ylabel('Player Rating')
plt.xlabel('Rank')
plt.title('Rank vs Player Rating by Amazon Price')


### Price
# %%
# %%
sns.scatterplot(x=games['list_price'],y=games['amazon_price'], hue=games['rank'],palette="flare")
plt.ylabel('Amazon Price')
plt.xlabel('List Price')
plt.title('List Price vs Amazon Price')

# %%
sns.boxplot(y=games['amazon_price'],x=games['min_players'])
plt.ylabel('Amazon Price')
plt.xlabel('Minimum Number of Players')
plt.yticks(np.arange(0, 860, step=50))
plt.title('Amazon Price vs Minimum Number of Players')
plt.savefig("visuals/pricevsMinPlayers.png",bbox_inches='tight',pad_inches=.1)


# %%
sns.scatterplot(x=games['rank'],y=games['amazon_price'])
plt.ylabel('Amazon Price')
plt.xlabel('Rank')
plt.yticks(np.arange(0, 860, step=50))
plt.title('Rank vs Amazon Price')

# %%

### Players
# %%
cleaned_players_games = games[games['max_players']<50]

# %%
sns.boxplot(x=cleaned_players_games['min_players'],y=cleaned_players_games['max_players'])
plt.ylabel('Maximum Number of Players')
plt.xlabel('Minimum Number of Players')
plt.yticks(np.arange(0, 21, step=2))
plt.title('Minimum vs Maximum Number of Players')
print(cleaned_players_games.groupby('min_players').mean(numeric_only=True)['max_players'].round(2))

# %%
sns.boxplot(x=games['min_players'],y=games['playing_time']/60)
plt.ylabel('Playing Time (Hours)')
plt.xlabel('Minimum Number of Players')
plt.title('Minimum Number of Players vs Average Playing Time')
plt.yticks(np.arange(0, 21, step=2))
games_sans_encoding[games_sans_encoding['playing_time']>240].iloc[:,[0,1,4,6,7,8,9]]
plt.savefig("visuals/minPlayersvsPlayTime.png",bbox_inches='tight',pad_inches=.1)


## Removes 1200 and 1000 hour games
# %%
games_sans_max_playing_time = games_sans_encoding[games_sans_encoding['playing_time']<800]
sns.boxplot(x=games_sans_max_playing_time['min_players'],y=games_sans_max_playing_time['playing_time']/60)
plt.ylabel('Playing Time (Hours)')
plt.xlabel('Minimum Number of Players')
plt.title('Minimum Number of Players vs Average Playing Time (Cleaned)')
# plt.yticks(np.arange(0, 21, step=2))
games_sans_encoding[games_sans_encoding['playing_time']>240].iloc[:,[0,1,4,6,7,8,9]]
plt.savefig("visuals/minPlayersvsPlayTimeEdited.png",bbox_inches='tight',pad_inches=.1)


# %%
sns.boxplot(x=games['max_players'],y=games['playing_time']/60)
plt.ylabel('Playing Time (Hours)')
plt.xlabel('Maximum Number of Players')
plt.title('Maximum Number of Players vs Average Playing Time')
plt.yticks(np.arange(0, 21, step=2))
games_sans_encoding[games_sans_encoding['playing_time']>240].iloc[:,[0,1,4,6,7,8,9]]

# %%
games_sans_max_playing_time = games_sans_encoding[games_sans_encoding['playing_time']<800]
sns.boxplot(x=games_sans_max_playing_time['max_players'],y=games_sans_max_playing_time['playing_time']/60)
plt.ylabel('Playing Time (Hours)')
plt.xlabel('Maximum Number of Players')
plt.title('Maximum Number of Players vs Average Playing Time (Cleaned)')
# plt.yticks(np.arange(0, 21, step=2))


### Year
# %%
games_sans_min_years = games_sans_encoding[games_sans_encoding['year']>1980]

# %%
sns.scatterplot(x=games_sans_min_years['year'],y=games_sans_min_years['amazon_price'],hue=games_sans_min_years['rank'],palette='flare')
plt.ylabel('Amazon Price')
plt.xlabel('Year Published')
plt.title('Year Published vs Price by Rank')
plt.savefig("visuals/yearvsPrice.png",bbox_inches='tight',pad_inches=.1)


# %%
sns.scatterplot(x=games_sans_min_years['year'],y=games_sans_min_years['rank'])
plt.ylabel('Rank')
plt.xlabel('Year Published')
plt.title('Year Published vs Rank')

# %%
sns.scatterplot(x=games_sans_min_years['year'],y=games_sans_min_years['playing_time']/60,hue=games_sans_min_years['rank'],palette='flare')
plt.ylabel('Playing Time (Hours)')
plt.xlabel('Year Published')
plt.yticks(np.arange(0, 21, step=2))
plt.xticks(np.arange(1980, 2026, step=5))
plt.title('Year Published vs Average Playing Time')
plt.savefig("visuals/yearvsPlayTime.png",bbox_inches='tight',pad_inches=.1)


