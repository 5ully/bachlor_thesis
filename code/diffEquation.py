# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 11:55:42 2021

@author: torge
"""
"""
========= ==================================================
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

import  numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.interpolate as si

KELVIN_CONST = 273.15

def initial_conditions(x_arr):
    f_arr = np.zeros(len(x_arr))
    for i, x in enumerate(x_arr):
        if x < 0.5:    
            f_arr[i] = x*2 + KELVIN_CONST
        else:
            f_arr[i] = 2-2*x + KELVIN_CONST
    return f_arr

def alpha_fun(k, Cp, ps):
    return k/(ps*Cp)

def model():
    dx = 0.1 # cm
    dt = 0.01 # s
    Nt = 10000000
    # x_array = np.arange(0,1+dx,dx)
    t_array = np.arange(0, dt*Nt, dt)
    print(t_array)
    # Nx = len(x_array)
    k = 0.33
    Cp = 0.06
    ps = 225
    alpha = alpha_fun(k, Cp, ps) 
    
    print("dt less than: ", dx**2/(2*alpha))
    
    


def plot_heat_diffusion(interpol_fun):

    dx = 0.1 # m
    dt = 1 # s
    Nt = 6000 #Time
    depth = 10.0 #m By increasing 
    x_array = np.arange(0,depth+dx,dx)
    t_array = np.arange(0, dt*Nt, dt)
    Nx = len(x_array)
    k = 0.33
    Cp = 0.06
    ps = 225
    alpha = alpha_fun(k, Cp, ps)
    
    heat_array = np.zeros((Nt, Nx))
    
    # Set initial conditions
    # heat_array[0, :] = initial_conditions(in)
    heat_array[0, :] = KELVIN_CONST
    
    # Set boundary condition
    heat_array[:, 0] = KELVIN_CONST
    heat_array[:,-1] = interpol_fun(t_array) + KELVIN_CONST
    print(heat_array[:,-1])
    
    k = alpha**2*dt/dx**2
    print("dt less than: ", dx**2/(2*alpha))
    for i in range(Nt-1):
        # Faster implementation
        a1 = heat_array[i, :-2]
        a2 = heat_array[i, 1:-1]
        a3 = heat_array[i, 2:]
        
        heat_array[i+1, 1:-1] = k*(a1-2*a2+a3) + a2
        
        # More understandable implementation
        # for j in range(1, Nx-1):
        #     du = k*(heat_array[i, j+1] - 2*heat_array[i,j] + heat_array[i,j-1])
        #     heat_array[i+1,j] = heat_array[i,j]+du
        
    print(len(heat_array[0]))
    #print(heat_array)
    sns.heatmap(heat_array)
    plt.show()
    np.savetxt()
    
    # fig, ax = plt.subplots(1)
    
    # arrayLength = len(heat_array)
    # print(arrayLength[:,0])
    
    # ax.plot(heat_array[0, :], label = "0")
    # ax.plot(heat_array[1/arrayLength, :], label = "1000")
    # ax.plot(heat_array[20000, :], label = "2000")
    # ax.plot(heat_array[40000, :], label = "4000")
    # ax.plot(heat_array[80000, :], label = "8000")
    # ax.plot(heat_array[99999, :], label = "9999")
    
    # plt.legend()
    # plt.show()
    
    fig, ax = plt.subplots(1)
    hours = t_array/3600
    ax.plot(hours, heat_array[:,-6], label = "5")
    ax.plot(hours, heat_array[:,-11], label = "10")
    # ax.plot(hours, heat_array[:,-9], label = "9")
    # ax.plot(hours, heat_array[:,-7], label = "7")
    ax.plot(hours, heat_array[:,-21], label = "20")
    ax.plot(hours, heat_array[:,-41], label = "40")
    ax.plot(hours, heat_array[:,-81], label = "80")
    # ax.plot(hours, heat_array[:,-2], label = "1")
    ax.plot(hours, heat_array[:,-1], label = "Recorded temp")
    plt.xlabel("Time [h]")
    plt.ylabel("Temperature [K]")
    plt.legend(loc = 1, title = "Depth [cm]")
    plt.show()
    
def get_temp_data(filename):
    df = pd.read_csv(filename, skiprows = 1, header = 0, nrows = 100000) 
    
    # Drop test rows
    df.drop(axis = 0, labels = [0,1,2,3,4], inplace = True)
    df = df.drop(df.index[0:55733])
    df.to_csv('df', index = False)
    #reset index
    df.reset_index(inplace = True)
    
    
    
    df['Timestamp'] = pd.to_datetime(df["TIMESTAMP"])
    df['Time'] = df['Timestamp'].dt.time
    # print(df["Time"])
    df["Elapsed time"] = (df["Timestamp"] - df["Timestamp"][0]).dt.total_seconds()
    # print(df["Elapsed time"])
    df["Temperature_Avg"] = df["Temperature_Avg"].astype(float)
    
    #ax = df.plot.scatter(x = "Elapsed time", y = "Temperature_Avg")
    
    
    df["Rolling mean"] = df.Temperature_Avg.rolling(window = 5, min_periods = 1).mean()

    interpol_fun = si.interp1d(x = df["Elapsed time"], y = df["Rolling mean"])
    #print(df["Rolling"])
    df.plot(x = "Elapsed time", y = ["Rolling mean", "Temperature_Avg"], kind = 'line')
    
    # Generate new timeseries
    # t_array = np.arange(0, 50000, 10)
    # interp_temp = interpol_fun(t_array)
    # ax.plot(t_array, interp_temp, color = "r")
    
    # interp_spline_temp = interpol_spline_fun(t_array)
    #ax.plot(t_array, interp_spline_temp, color = "y")
    
    return interpol_fun

def temp_solution(filename):
    df = pd.read_csv(filename, skiprows= 1, header = 0, nrows = 100000)
    
    # Drop test rows
    df.drop(axis = 0, labels = [0,1,2,3,4], inplace = True)
    df = df.drop(df.index[0:55733])
    df.to_csv('df', index = False)
    #reset index
    df.reset_index(inplace = True)
    
    #Get and draw temp profiles
    df['Timestamp'] = pd.to_datetime(df["TIMESTAMP"])
    df['Time'] = df['Timestamp'].dt.time
    # print(df["Time"])
    df["Elapsed time"] = (df["Timestamp"] - df["Timestamp"][0]).dt.total_seconds()
    # print(df["Elapsed time"])
    df["Temperature_Avg"] = df["Temperature_Avg"].astype(float)
    
    
    
    

if __name__ == "__main__":
    # filename = r'..\data\PC200W\HVL_TableMem.dat' Testfile
    filename = r'..\data\PC200W2\CR1000_TableMem.dat'
    temp_data = get_temp_data(filename)
    plot_heat_diffusion(temp_data)
