# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import plotly.express as px

# Import data
df = pd.read_csv(r'C:\Users\lenovo\Documents\Downloads\NBALineup2021.csv')

# Title for app
st.set_page_config(layout="wide")
st.title('NBA Lineup Analysis Tool')

# User chooses team 
team = st.selectbox(
     'Choose Your Team:',
     df['team'].unique())

# Get just the selected team 
df_team = df[df['team'] == team].reset_index(drop=True)

# Get players on roster
df_team['players_list'] = df_team['players_list'].str.replace(r"[\"\' \[\]]", '').str.split(',')
duplicate_roster = df_team['players_list'].apply(pd.Series).stack()
roster = duplicate_roster.unique()

players = st.multiselect(
     'Select your players',
     roster,
     roster[0:5])

# Find the right lineup
df_lineup = df_team[df_team['players_list'].apply(lambda x: all(player in x for player in players))]

# Create a DataFrame with important statistics
df_important = df_lineup[['GROUP_NAME', 'REB', 'AST', 'PTS_RANK', 'FGA', 'PTS', 'BLK']]

# Display the important DataFrame
st.dataframe(df_important)

# Check if df_important is empty and print columns
if df_important.empty:
    st.write("DataFrame is empty.")
else:
    st.write("DataFrame columns:", df_important.columns.tolist())
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1: 
        fig_min = px.histogram(df_team, x="REB", title="Rebounds Distribution")
        fig_min.add_vline(x=df_important['REB'].values[0], line_color='red')
        st.plotly_chart(fig_min, use_container_width=True)

    with col2: 
        fig_2 = px.histogram(df_team, x="AST", title="Assists Distribution")
        fig_2.add_vline(x=df_important['AST'].values[0], line_color='red')
        st.plotly_chart(fig_2, use_container_width=True)
        
    with col3: 
        fig_3 = px.histogram(df_team, x="PTS_RANK", title="Points Rank Distribution")
        fig_3.add_vline(x=df_important['PTS_RANK'].values[0], line_color='red')
        st.plotly_chart(fig_3, use_container_width=True)
        
    with col4: 
        fig_4 = px.histogram(df_team, x="FGA", title="Field Goals Attempted Distribution")
        fig_4.add_vline(x=df_important['FGA'].values[0], line_color='red')
        st.plotly_chart(fig_4, use_container_width=True)
    
    with col5: 
        fig_5 = px.histogram(df_team, x="PTS", title="Points Distribution")
        fig_5.add_vline(x=df_important['PTS'].values[0], line_color='red')
        st.plotly_chart(fig_5, use_container_width=True)

    # Display the top players based on various statistics
    st.subheader("Top Players Based on Statistics")
    
    # Most Points Scored
    top_pts = df_team.nlargest(5, 'PTS')[['players_list', 'PTS']]
    st.write("Top 5 Players by Points Scored:")
    st.dataframe(top_pts)

    # Most Assists
    top_assists = df_team.nlargest(5, 'AST')[['players_list', 'AST']]
    st.write("Top 5 Players by Assists:")
    st.dataframe(top_assists)

    # Most Rebounds
    top_rebounds = df_team.nlargest(5, 'REB')[['players_list', 'REB']]
    st.write("Top 5 Players by Rebounds:")
    st.dataframe(top_rebounds)

    # Most Blocks
    top_blocks = df_team.nlargest(5, 'BLK')[['players_list', 'BLK']]
    st.write("Top 5 Players by Blocks:")
    st.dataframe(top_blocks)

    # Points Rank
    top_pts_rank = df_team.nsmallest(5, 'PTS_RANK')[['players_list', 'PTS_RANK']]
    st.write("Top 5 Players by Points Rank (Lower is Better):")
    st.dataframe(top_pts_rank)