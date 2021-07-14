# -*- coding: utf-8 -*-
"""
Created on Sun Nov  29 12:08:01 2020

@author: hp
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import ticker
#from StockQutoes import sq

def retrieve_parameters(tickerSymbol, startDate, endDate):
    return tickerSymbol, startDate, endDate

#use matplotlib to plot the graphs
def closing_price_vs_time(data, tickerSymbol, startDate, endDate):
    fig, ax = plt.subplots()
    time = data.index
    closing_price = data['Close']
    plt.figure(figsize=(14,7))
    plt.title("Closing price vs Date of {} within date range {} to {}".format(tickerSymbol.upper(), startDate, endDate))
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.plot(time, closing_price, color = "blue", label = "Closing Price")
    fig.autofmt_xdate()
    plt.legend()
    download_plot(tickerSymbol.upper() + '_CLOSE.png')
    plt.show()

    change_parameter_message()
        
def adjClose_vs_time(data, tickerSymbol, startDate, endDate):
    fig, ax = plt.subplots()
    xAxis = data.index
    closeParametery2 = data['Adj Close']
    plt.figure(figsize=(14,7))
    plt.title('Adj Close vs Time Graph for {} between {} and {}'.format(tickerSymbol.upper(), startDate, endDate))
    plt.xlabel('Date')
    plt.ylabel('Adj Close')
    plt.plot(xAxis, closeParametery2, color = 'blue', label='Adj Close')    #  
    fig.autofmt_xdate()
    plt.legend()
    download_plot(tickerSymbol.upper() + '_ADJC.png')
    plt.show()

    change_parameter_message()
    
    
def open_vs_close(data, tickerSymbol, startDate, endDate):
    fig, ax = plt.subplots()
    xAxis = data.index
    openParametery1 = data['Open']
    closeParametery2 = data['Close']
    plt.figure(figsize=(14,7))
    plt.xlabel('Date')
    plt.ylabel('Open and Close Prices')
    plt.title('Open vs Close vs Date plot for {} within the date range {} to {}'.format(tickerSymbol.upper(), startDate, endDate))
    plt.plot(xAxis, openParametery1, color = "r", label = "Open")
    plt.plot(xAxis, closeParametery2, color = "blue",  label="Close")
    fig.autofmt_xdate()
    plt.legend()
    download_plot(tickerSymbol.upper() + '_OC.png')
    plt.show()

    change_parameter_message()
    
    
def moving_average(data, tickerSymbol, startDate, endDate):
    movingWindow = int(input("Please enter the moving window: "))
    closeParameter = data['Close']
    movingAverage = closeParameter.rolling(window=movingWindow).mean()
    print("Moving Average: ", movingAverage)
    plt.figure(figsize=(14,7))
    plt.ylabel('Closing Price')
    plt.title("Moving Average vs Closing Price vs Date of {} within date range {} to {} for moving window {}".format(tickerSymbol.upper(), startDate, endDate, movingWindow))
    closeParameter.plot(label="Closing Price")
    movingAverage.plot(label="Moving Average")
    plt.legend()
    download_plot(tickerSymbol.upper() + '_MA.png')
    plt.show()

    change_parameter_message()
    
    
def weighted_moving_average(data, tickerSymbol, startDate, endDate):
    moving_window = input("Please provide a moving window: ")
    data['Close_moving_avg_n']=data.iloc[:,3].rolling(window=int(moving_window)).mean()
    print(data)
    int_moving_window=int(moving_window)
    weights=np.arange(1,int_moving_window+1)
    print(weights)
    data['WMA'] = data['Close'].rolling(int_moving_window).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
    print(data)
    plt.figure(figsize=(16,9))
    data[['Close','Close_moving_avg_n','WMA']].plot(linestyle='dashed')    
    plt.title('Close Price vs Close price Moving Average vs Close Weighted Moving Average of {} for moving window {}'.format(tickerSymbol.upper(), moving_window))
    plt.ylabel('Price')
    download_plot(tickerSymbol.upper() + '_WMA.png')
    plt.show()

    change_parameter_message()
    

def moving_average_convergence_divergence(data, tickerSymbol, startDate, endDate):
    short_window = int(input("Enter the short window: "))
    long_window = int(input("Enter the long window: "))
    signalPeriod = int(input("Enter the signal period: "))
    closing_price = data['Close']
    print(closing_price)
    short = closing_price.ewm(span = short_window, adjust = False).mean()
    long = closing_price.ewm(span = long_window, adjust = False).mean()
    macd = short - long
    signal = closing_price.ewm(span = signalPeriod, adjust = False).mean()
    print(macd)
    print(signal)
    
    fig, ax = plt.subplots()
    plt.figure(figsize=(14,7))
    plt.title('Moving Average Convergence Divergence for {} within date range {} to {}'.format(tickerSymbol.upper(), startDate, endDate))
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.plot(data.index, macd, color='blue', label='MACD')
    plt.plot(data.index, signal, color='r', label='Signal')
    fig.autofmt_xdate()
    plt.legend()
    download_plot(tickerSymbol.upper() + '_MACD.png')
    plt.show()
    
    change_parameter_message()
    
    
def linear_trend_lines(data, tickerSymbol, startDate, endDate):
    #divide x axis into n parts of data between 0 and 1
    date = np.linspace(0, 1, len(data.index))
    closingPrice = data['Close']
    #Create Polynomial fit of degree 1
    poly_fit = np.polyfit(date, closingPrice, 1)
    #Fit the 1 degree equation into ID
    polyid = np.poly1d(poly_fit)
    #get the y axis trend
    trend = polyid(date)
    
    #Plot the linear line graph
    plt.figure(figsize=(14,7))
    plt.title("Linear trendline for {} from {} - {}".format(tickerSymbol, startDate, endDate))
    plt.scatter(data.index, data.Close, label="Closing Price")
    plt.plot(data.index, trend, "r", label="Linear Trend for Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend()
    download_plot(tickerSymbol.upper() + '_LTL.png')
    plt.show()
    
    change_parameter_message()
    
    

def change_parameter_message():
    print("\nThe plot is visible in the 'Plots' tab \n")
    print("If you want to view technical indicator graphs for another Ticker Symbol and date ramge,",
          "Enter 8 to exit the data visualization sub-menu, 0 to exit main menu, and enter 3 to input",
          "your new parameters. Else, continue inputting other options to plot graphs for existing parameters.")

def save_plot(filename):
    plt.savefig(filename)
    
def download_plot(filename):
    user_answer = input("Do you want to save the map in .png format? \nIf yes, please press Y else press N: ")
    if(user_answer == 'Y'):
        save_plot(filename)