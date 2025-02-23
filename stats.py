#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Set the title of the app
st.title("NBA Player Statistics Analysis")

# Load the data
df = pd.read_csv(r"./pages/NBALineup2021.csv")

# Display the first few rows of the dataframe
st.subheader("Data Preview")
st.write(df.head())

# Select relevant columns
df = df[['GROUP_NAME', 'PTS', 'AST', 'REB', 'MIN']]

# Check for null values
st.subheader("Missing Values")
st.write(df.isnull().sum())

# Drop rows with missing values
df.dropna(inplace=True)

# Prepare the data for modeling
X = df[['PTS', 'AST', 'REB']]
y = df['MIN']
X = sm.add_constant(X)

# Convert columns to numeric
for col in ['PTS', 'AST', 'REB', 'MIN']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing values again after conversion
df.dropna(inplace=True)

# Prepare the data for modeling again
X = df[['PTS', 'AST', 'REB']]
y = df['MIN']
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# Display the model summary
st.subheader("Model Summary")
st.text(model.summary())

# Create pairplot
st.subheader("Pairplot of Player Statistics")
pairplot_fig = sns.pairplot(df, x_vars=['PTS', 'AST', 'REB'], y_vars='MIN', height=5, aspect=0.7)
plt.suptitle('Player Statistics vs. Minutes Played', y=1.02)
st.pyplot(pairplot_fig)

# Create scatter plots
st.subheader("Scatter Plots")
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

sns.scatterplot(data=df, x='PTS', y='MIN', ax=axs[0])
axs[0].set_title('Points vs. Minutes Played')

sns.scatterplot(data=df, x='AST', y='MIN', ax=axs[1])
axs[1].set_title('Assists vs. Minutes Played')

sns.scatterplot(data=df, x='REB', y='MIN', ax=axs[2])
axs[2].set_title('Rebounds vs. Minutes Played')

plt.tight_layout()
st.pyplot(fig)