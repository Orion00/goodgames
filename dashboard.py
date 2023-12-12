# %%
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import string
import seaborn as sns

# %%
games = pd.read_csv("data/full_data.csv")
games_sans_encoding = games.iloc[:,0:11]
games_sans_encoding = games_sans_encoding.drop('game_id',axis=1)
games_sans_year_extremes = games_sans_encoding[games_sans_encoding['year']>1980]
df = games
# %%
st.title("BGG Top 500 Games Exploration")


st.write("Filter by name and/or year published")
selected_game_name = st.text_input("Enter a game name")
selected_year_range = st.slider("Enter a year range",games_sans_year_extremes['year'].unique().min(),games['year'].unique().max(),(1980,2023))
games_filtered = games.loc[(games['year']>=selected_year_range[0]) & (games['year']<=selected_year_range[1])]
if selected_game_name:
    games_filtered = games_filtered.loc[games_filtered['title'].str.lower().str.contains(selected_game_name.lower())]
if len(games_filtered) == 0:
    st.write("Sorry, no games are available with those filters.")
else:
    st.write(games_filtered.iloc[:,0:11])

games_mechanics = (games_filtered.iloc[:,12:].sum(axis=0)).sort_values(ascending=False)
num_mechanics = min(15,len(games_mechanics[games_mechanics>0]))
games_mechanics = games_mechanics.head(num_mechanics).sort_values(ascending=True)
if len(games_mechanics) != 0:
    fig = px.bar(x=games_mechanics.values,y=games_mechanics.index,color=games_mechanics.index,
                 labels={
                     "x": "Mechanic Frequency",
                     "y": "Mechanic",
                 })
# st.pyplot(fig)
    t = str(num_mechanics)+" Most Frequent Mechanics"
    fig.update_layout(title=t,showlegend=False)
    st.write(fig)


# name_df = df[df["name"] == selected_name]

# if name_df.empty:
#     st.write("Name not found")
# else:
#     fig = px.line(name_df,x='year',y='n',color='sex',
#                   color_discrete_sequence=px.colors.qualitative.Set2)
#     st.plotly_chart(fig)

# selected_year = st.selectbox("Select a year",df['year'].unique())

# year_df = df[df["year"] == selected_year]

# girl_names = year_df[year_df["sex"]=="F"].sort_values(by='n',ascending=False).head()['name'].reset_index(drop=True)
# boy_names = year_df[year_df["sex"]=="M"].sort_values(by='n',ascending=False).head()['name'].reset_index(drop=True)
# top_names = pd.concat([girl_names,boy_names],axis=1)
# top_names.columns = ['girl','boy']
# st.write(f"Top names in {selected_year}")
# st.write(top_names)