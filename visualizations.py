# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
games = pd.read_csv("data/full_data.csv")

# %%
# games = games[0:25]
mechanics_counts = games.iloc[:,-91:].sum(axis=0).sort_values(ascending=False).head(15)

# %%
sns.barplot(y=mechanics_counts.index,x=mechanics_counts.values,palette="Set2")
plt.ylabel('Mechanics')
plt.xlabel('Frequency')
plt.title('Most Frequent Mechanics in Top 500 Games')
plt.savefig("visuals/mostFreqMechanics.png",bbox_inches='tight',pad_inches=.1)