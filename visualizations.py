# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
game = pd.read_csv("full_data.csv")

# %%
game = game[0:25]
mechanics_counts = game.iloc[:,-91:].sum(axis=0).sort_values(ascending=False).head(21)

# %%
sns.barplot(y=mechanics_counts.index,x=mechanics_counts.values,)
plt.ylabel('Mechanics')
plt.xlabel('Frequency')
plt.title('Most Frequent Mechanics in Top 25 Games')
plt.show()