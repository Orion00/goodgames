### Imports
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

games = pd.read_csv("data/full_data.csv")



### Mechanics 
# %%
mechanics_counts = games.iloc[:,-91:].sum(axis=0).sort_values(ascending=False).head(15)
sns.barplot(y=mechanics_counts.index,x=mechanics_counts.values,palette="Set2")
plt.ylabel('Mechanics')
plt.xlabel('Frequency')
plt.title('Most Frequent Mechanics in Top 500 Games')
plt.savefig("visuals/mostFreqMechanics.png",bbox_inches='tight',pad_inches=.1)

### Rating
# %%
sns.scatterplot(x=games['BGG_rating'],y=games['avg_rating'], hue=games['rank'],palette="flare")
plt.ylabel('Player Rating')
plt.xlabel('BGG Rating')
plt.title('BGG Rating vs Player Rating')

# %%
sns.scatterplot(x=games['list_price'],y=games['avg_rating'], hue=games['rank'],palette="flare")
plt.ylabel('Player Rating')
plt.xlabel('List Price')
plt.title('List Price vs Player Rating')

# %%
sns.scatterplot(x=games['rank'],y=games['avg_rating'])
plt.ylabel('Player Rating')
plt.xlabel('Rank')
plt.title('Rank vs Player Rating')

 # %%
sns.scatterplot(x=games['rank'],y=games['avg_rating'], hue=games['list_price'],palette="flare")
plt.ylabel('Player Rating')
plt.xlabel('Rank')
plt.title('Rank vs Player Rating by List Price')


### Price
sns.scatterplot(x=games['list_price'],y=games['amazon_price'], hue=games['rank'],palette="flare",dropna=True)
plt.ylabel('Player Rating')
plt.xlabel('List Price')
plt.title('List Price vs Player Rating')

# %%
games