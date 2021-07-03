"""
===========================================================
                    Imports
===========================================================
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as d
import pandas as pd
import datetime as dt



"""
Function for solving 1D diffusion in the snowpack with
with boundary conditions.
for information on the physical derivation use this:
https://ocw.mit.edu/courses/mathematics/18-303-linear-partial-differential-equations-fall-2006/lecture-notes/heateqni.pdf

The following naming conventions for the variables are used:

ll ========= ==================================================
Name      Description
========= ==================================================
dt        Time step (s)
dx        Distance step (cm)
k         Thermal Conductivity (W*m^(−1)*K^(-1))
ps         Density (kg/m³)
Cp        Specific Heat Capacity (J/kg C°)
a         Thermal diffusivity (m^2/s) (k/(ps*Cp))
u         Temperature (K)
x         Depth of Snow (m)
t         Time (s)

y         Trigonometric function to calculate for daily temperature changes
A         Amplitude (Absolut value)
B         2π/B is the period
C         Vertical Translations
D         Horizontal Translations

filename  Path of the file
row_skip  Number of rows to skip at the top of the sheet
col_index Column index where the time serie is located
"""
filename = r'..\data\PC200W2\data.txt'

"""
================================================================
                        Import files ++
================================================================
"""
df = pd.read_csv(filename, skiprows = 1, header = 0) 

# Drop test rows
df.drop(axis = 0, labels = [0,1], inplace = True)
df["ShortwaveRadiationIn_Avg"] = df["ShortwaveRadiationIn_Avg"].astype("float")
df["ShortwaveRadiationOut_Avg"] = df["ShortwaveRadiationOut_Avg"].astype("float")
# df["LongwaveRadiationIn_Avg"] = df["LongwaveRadiationIn_Avg"].astype("float")
# df["LongwaveRadiationOut_Avg"] = df["LongwaveRadiationOut_Avg"].astype("float")


#print(df.head())


"""
===================== Section ==============================
                Trigonometric Function
============================================================
"""

"""
Test section for trigonometric function
"""
"""
===========================================================
                    Munge sequence
===========================================================

"""

df['Timestamp'] = pd.to_datetime(df["TIMESTAMP"])
df['Time'] = df['Timestamp'].dt.time
# df = df.groupby('Time').describe().unstack()

"""
===========================================================
                    Draw
===========================================================
"""


fig, ax = plt.subplots(1, figsize=(12,6))
ax.set_title('', fontsize = 14)
ax.set_ylabel('Radiation', fontsize = 14)
ax.set_xlabel('Year', fontsize = 14)

#ax.plot(df.index, df["Time"]['mean'], 'g', linewidth = 2.0)
# ax.plot(df["Timestamp"], df["ShortwaveRadiationIn_Avg"]+df["LongwaveRadiationIn_Avg"], 'g', linewidth = 2.0, alpha = 0.7, label = "Total Radiation Inn")
# ax.plot(df["Timestamp"], df["ShortwaveRadiationOut_Avg"]+df["LongwaveRadiationOut_Avg"], 'r', linewidth = 2.0, alpha = 0.7, label = "Total Radiation Out")
ticks = ax.get_xticks()
ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours = 3)), 5))
ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours = 3)), 25), minor = True)
#ax.xaxis.set_major_formatter(d.DateFormatter('%I:%M %p'))

plt.legend()
plt.tight_layout()
plt.show()




fig, ax2 = plt.subplots(1, figsize = (12, 6))
ax.set_title('', fontsize = 14)
ax.set_ylabel('', fontsize = 12)
ax.set_xlabel('', fontsize = 12)

ticks = ax.get_xticks() 
ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours = 3)), 5))
ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours = 3)), 25), minor = True)


ax.plot(df['Timestamp'], df['TemperatureIce1m_Avg'], label = '1m')
ax.plot(df['Timestamp'], df['TemperatureIce2m_Avg'], label = '1m')
ax.plot(df['Timestamp'], df['TemperatureIce3m_Avg'], label = '1m')
ax.plot(df['Timestamp'], df['TemperatureIce4m_Avg'], label = '1m')
ax.plot(df['Timestamp'], df['TemperatureIce5m_Avg'], label = '1m')
ax.plot(df['Timestamp'], df['TemperatureIce6m_Avg'], label = '1m')
ax.plot(df['Timestamp'], df['TemperatureIce7m_Avg'], label = '1m')
ax.plot(df['Timestamp'], df['TemperatureIce10m_Avg'], label = '1m')

plt.legend()
plt.tight_layout()
plt.show()

