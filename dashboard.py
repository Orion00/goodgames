# %%
import pandas as pd
import streamlit as st
import plotly.express as px
import math

# %%
games = pd.read_csv("data/full_data.csv")
games_sans_encoding = games.iloc[:,0:11]
games_sans_encoding = games_sans_encoding.drop('game_id',axis=1)
games_sans_year_extremes = games_sans_encoding[games_sans_encoding['year']>1980]
df = games
# %%
st.title("BGG Top 500 Games Exploration")

st.markdown("## Filter Most Frequent Mechanics")


st.write("Filter by name, year published, and/or price")
selected_game_name = st.text_input("Enter a game name")
selected_year_range = st.slider("Enter a year range",games_sans_year_extremes['year'].unique().min(),games['year'].unique().max(),(1980,2023))
min_price = (games['amazon_price'].min())
max_price = (games['amazon_price'].max())

# selected_price = st.number_input("Enter a max price", min_value=min_price, max_value=max_price, value=max_price, format="%.2f $",step=5)
selected_price = st.number_input(
    "Enter a max price",
    min_value=min_price,
    max_value=max_price,
    step=5.0,
    value=max_price
)

games_filtered = games.loc[
    (games['year'] >= selected_year_range[0]) & 
    (games['year'] <= selected_year_range[1]) & 
    (games['amazon_price'] <= selected_price)
]
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
    t = str(num_mechanics)+" Most Frequent Mechanics"
    fig.update_layout(title=t,showlegend=False)
    st.write(fig)

if len(games_filtered) != 0:
    st.markdown("## Data Playground")
    st.write("Make your own scatterplots. Use whatever variables you prefer.")
    x_axis = st.selectbox("Select an X axis",['rank','year','min_players','max_players'])
    y_axis = st.selectbox("Select a Y axis",['BGG_rating','avg_rating','list_price','amazon_price'])
    color = st.selectbox("Select a color",['','rank','year','BGG_rating','avg_rating','list_price','amazon_price','min_players','max_players'])
    t = x_axis + " vs " + y_axis
    if color:
        t += ' by '+color
        fig = px.scatter(data_frame=games_filtered,x=x_axis,y=y_axis,color=color)
    else:
        fig = px.scatter(data_frame=games_filtered,x=x_axis,y=y_axis)
    fig.update_layout(title=t)
    st.write(fig)
