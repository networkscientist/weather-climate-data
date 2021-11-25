## This script aim to solve the exercises in the Weather Reconstruction tutorial on giub-torrent.unibe.ch/weather-simulation
# Load pandas
import pandas as pd
import math
import matplotlib.pyplot as plt

# Read CSV file into DataFrame df
df = pd.read_table('data/ClimateData_Homogenize_BreakDetection_Data.txt')
mean_cand = df['Candidate_T(degC)'].mean()
mean_ref = df['Reference_T(degC)'].mean()
df['norm_diff_accumulated']=0.0
def craddock_test():
    for index,row in df.iterrows():
        df.at[index+1,'norm_diff_accumulated'] = df.at[index,'norm_diff_accumulated'] + row['Reference_T(degC)'] - row['Candidate_T(degC)'] - (mean_ref - mean_cand)
craddock_test()

## Create figure and plot space
fig, ax = plt.subplots(figsize=(10, 10))

# ## Add x-axis and y-axis
# ax.scatter(x=df.index, y=df['norm_diff_accumulated'],color='purple')

## Set title and labels for axes
ax.set(xlabel="Time",
       ylabel='Temp (°C)',
       title="Temperature Plot")
plt.scatter(df.index,
            df['norm_diff_accumulated'])
plt.show()