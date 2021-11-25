## This script aim to solve the exercises in the Weather Reconstruction tutorial on giub-torrent.unibe.ch/weather-simulation
# Load pandas
import pandas as pd
import math
import matplotlib.pyplot as plt

## Processing
# Constants
gamma = 1.82 * pow(10, -4)
rho = 1.35951 * pow(10, 4)
h = 776
lat = 0.827635131295711
g_n = 9.80665
g_local = 9.80620 * (1 - 0.0026442 * math.cos(2 * lat) - 0.0000058 * (math.cos(2 * lat) ** 2)) - 0.000003086 * h
r = 287.05
a = 6.5e-03
Ts = 273.15
# Read CSV file into DataFrame df
df = pd.read_table('data/ClimateData_Process_Data.txt')

# Convert barometric length from Paris inch to mm
df['Pmm_Sunrise'] = df['Pressure_sunrise'] * 27.07
df['Pmm_Sunset'] = df['Pressure_Sunset'] * 27.07

# Convert Temperature from Réaumur to Celsius
df['Tc_Sunrise'] = df['Temperature_sunrise'] / (0.8)
df['Tc_Sunset'] = df['Temperature_Sunset'] / (0.8)

# Correct barometric length to 0°C; the factor (10/0.8) is used, since the pressure measurement has been corrected to 10°R already
df['L0_Sunrise'] = (1 - gamma * (10 / 0.8)) * df['Pmm_Sunrise']
df['L0_Sunset'] = (1 - gamma * (10 / 0.8)) * df['Pmm_Sunset']

# Convert pressure readings from mm to hPa
df['P0_Sunrise'] = rho * g_n * df['L0_Sunrise'] * pow(10, -5)
df['P0_Sunset'] = rho * g_n * df['L0_Sunset'] * pow(10, -5)

# Correct for local gravity
df['Pn_Sunrise'] = (g_local / g_n) * df['P0_Sunrise']
df['Pn_Sunset'] = (g_local / g_n) * df['P0_Sunset']

# Reduce to mean sea level
#df['SLP_Sunrise'] = df['Pn_Sunrise']*math.exp(((g_local/r)*h)/(df['Tc_Sunrise']+Ts+a*(h/2)))

## Quality Control
# 1. Test: Find physically impossible values
def qc_physical(col_name, value, boundary):
    """
    Checks wether a column in the DataFrame has physically impossible values.
    :param col_name:
    :param value:
    :param boundary:
    :return:
    """
    if boundary in ['high']:
        counter = 0
        for index, row in df.iterrows():
            if row[col_name] >= value:
                print(row)
                counter += 1
        print(counter, " possible error found")
    if boundary in ['low']:
        counter = 0
        for index, row in df.iterrows():
            if row[col_name] <= value:
                print(row)
                counter += 1
        print(counter, " possible error found")
# Physically impossible temperatures
print("QC: 1. Physically impossible values:")
qc_physical('Tc_Sunrise', -Ts, 'low')
qc_physical('Tc_Sunset', -Ts, 'low')

# Physically impossible pressures
qc_physical('Pn_Sunset', 0, 'low')
qc_physical('Pn_Sunrise', 0, 'low')

# 2. Test: Find physically implausible values:
# Physically implausible values
print("QC: 2. Physically implausible values:")
qc_physical('Tc_Sunrise', -80, 'low')
qc_physical('Tc_Sunrise', 60, 'high')
qc_physical('Tc_Sunset', -80, 'low')
qc_physical('Tc_Sunset', 60, 'high')

qc_physical('Pn_Sunset', 500, 'low')
qc_physical('Pn_Sunset', 1100, 'high')
qc_physical('Pn_Sunrise', 500, 'low')
qc_physical('Pn_Sunrise', 1100, 'high')

# 3. Test: Are there outliers outside +-Std.Dev?
print("QC: 3. Statistically implausible values:")
def qc_statistical(col_name):
    for index, row in df.iterrows():
        if row[col_name] >= (df[col_name].mean() + 4*df[col_name].std()):
            counter = 0
            print(row)
            counter += 1
            print(counter, " possible error found")
    for index, row in df.iterrows():
        if row[col_name] <= (df[col_name].mean() - 4*df[col_name].std()):
            counter = 0
            print(row)
            counter += 1
            print(counter, " possible error found")

qc_statistical('Tc_Sunset')
qc_statistical('Tc_Sunrise')
qc_statistical('Pn_Sunset')
qc_statistical('Pn_Sunrise')

# 4. Test: Sequence Analysis - Are there huge difference for consecutive days? Are there too many same values for consecutive days?
print("QC: 4. Sequence Analysis:")
def qc_sequence_diff(col_name, difference):
    for index, row in df.iterrows():
        try:
            if abs(df.at[index,col_name]-df.at[index+1,col_name]) >= difference:
                # counter = 0
                print("Possible error found:")
                print("Value 1: ", df.at[index,col_name], " Row: ", index)
                print("Value 2: ", df.at[index+1,col_name], " Row: ", index+1)
                # counter += 1
                # print(counter, " possible error found")
        except KeyError:
            continue

def qc_sequence_same(col_name):
    for index, row in df.iterrows():
        try:
            if df.at[index,col_name] == df.at[index+1,col_name] == df.at[index+2,col_name]== df.at[index+3,col_name]:
                print("Possible error found:")
                print("Value: ", df.at[index,col_name], " Rows: ", index, " to ", index+3)
        except KeyError:
            continue

#Test for huge differences between 2 consecutive days
qc_sequence_diff('Tc_Sunset', 25)
qc_sequence_diff('Tc_Sunrise', 25)
qc_sequence_diff('Pn_Sunset', 40)
qc_sequence_diff('Pn_Sunrise', 40)
#Test for same values on four consecutive days
qc_sequence_same('Tc_Sunset')
qc_sequence_same('Tc_Sunrise')
qc_sequence_same('Pn_Sunset')
qc_sequence_same('Pn_Sunrise')
## Create figure and plot space
fig, ax = plt.subplots(figsize=(10, 10))

## Add x-axis and y-axis
ax.scatter(x=df.index, y=df['Pn_Sunrise'],color='purple')

## Set title and labels for axes
ax.set(xlabel="Time",
       ylabel='Temp (°C)',
       title="Temperature Plot")
plt.scatter(df.index,
            df['Pn_Sunrise'])
plt.show()
# Step 1: Physically Impossible Values
# Show dataframe
print(df)
