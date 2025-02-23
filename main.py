import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set the title of the app
st.title("NBA Data Analysis for 2021 Season")

# Load the dataset
df = pd.read_csv(r'pages\NBALineup2021.csv')

# Display the top rows of the dataset
st.subheader("First rows of the dataset:")
st.write(df.head())

# Data Cleaning
# Check for missing values
st.subheader("Missing values in each column:")
st.write(df.isnull().sum())

# Drop rows with missing values (if any)
df.dropna(inplace=True)

# Convert relevant columns to appropriate data types if necessary
df['W_RANK'] = df['W_RANK'].astype(int)

# Basic Analysis
# Calculate total points by team
team_points = df.groupby('team')['PTS'].sum().reset_index()
best_steam = team_points.loc[team_points['PTS'].idxmax()]
st.subheader("Team with the Best Performance:")
st.write("Best Team by Points:", best_steam)
# Assuming you have a DataFrame `df` with a 'team' and 'AST' column
team_assists = df.groupby('team')['AST'].sum().reset_index()  # Create a DataFrame with total assists per team
best_team = team_assists.loc[team_assists['AST'].idxmax()]  # Get the team with the maximum assists
st.write("Best Team by Assists:", best_team)

team_rebounds = df.groupby('team')['REB'].sum().reset_index()  # Create a DataFrame with total assists per team
best_team = team_rebounds.loc[team_rebounds['REB'].idxmax()]  # Get the team with the maximum assists
st.write("Best Team by Rebounds:", best_team)

team_blocks = df.groupby('team')['BLK'].sum().reset_index()  # Create a DataFrame with total assists per team
best_team = team_blocks.loc[team_blocks['BLK'].idxmax()]  # Get the team with the maximum assists
st.write("Best Team by Blocks:", best_team)



best_team_data = df[df['team'] == best_steam['team']]

# Display all rows for the best team
st.subheader(f"All Rows for leading points {best_steam['team']}:")
st.write(best_team_data)

# Visualization: Total Points by Team
st.subheader("Total Points by Team in 2021 NBA Season")
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(team_points['team'], team_points['PTS'], color='blue')
ax.set_xlabel('Team')
ax.set_ylabel('Total Points')
ax.set_title('Total Points by Team in 2021 NBA Season')
plt.xticks(rotation=90)
st.pyplot(fig)  # Use st.pyplot to display the figure in Streamlit

# Additional Analysis: Blocks, Steals, Rebounds, Assists
summary_stats = df.groupby('team')[['BLK', 'STL', 'REB', 'AST', 'FG3A', 'FG3M']].sum().reset_index()

# Display the summary statistics
st.subheader("Summary Statistics by Team:")
st.write(summary_stats)

# Visualization: Blocks, Steals, Rebounds, and Assists by Team
st.subheader("Summary Statistics by Team")
fig2, ax2 = plt.subplots(figsize=(12, 6))
summary_stats.set_index('team').plot(kind='bar', ax=ax2)
ax2.set_title('Summary Statistics by Team in 2021 NBA Season')
ax2.set_ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(fig2)  # Use st.pyplot to display the figure in Streamlit

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_NBALineup2021.csv', index=False)