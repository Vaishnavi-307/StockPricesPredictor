# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 00:56:07 2020

@author: hp
"""

#import libraries
import yfinance as yf
import DataVisualizationLogic as dvl

#get the ticker symbol and date range
def get_parameters(tickerSymbol, startDate, endDate):
    tickerSymbol = input("Please choose ticker symbol: ")
    startDate = input("Please input the start date (YYYY-MM-DD): ")
    endDate = input("Please input the end date (YYYY-MM-DD): ")
    return tickerSymbol, startDate, endDate

#display the sub-menu for visualization
def visualization_menu():
    print("\n")
    print("Welcome to the Data visualization board.\nThe following are your choices: \n")
    print("1. Closing Price vs Time \n2. Adjacent Closing Price vs Time \n3. Open and Closing Prices vs Time",
          " \n4. Moving Average \n5. Weighted Moving Average \n6. Moving Average Convergence/Divergence",
          "\n7. Linear Trend Lines \n")
    
#take user's choice    
def get_visualization_choice():
    return input("Please enter your choice to create plots (8 to exit): ")

#process user's choice
def process_choice(choice, data, tickerSymbol, startDate, endDate):
    while (choice != "8"):
        if(choice == "1"):
            dvl.closing_price_vs_time(data, tickerSymbol, startDate, endDate)
        elif(choice == "2"):
            dvl.adjClose_vs_time(data, tickerSymbol, startDate, endDate)
        elif(choice == "3"):
            dvl.open_vs_close(data, tickerSymbol, startDate, endDate)
        elif(choice == "4"):
            dvl.moving_average(data, tickerSymbol, startDate, endDate)
        elif(choice == "5"):
            dvl.weighted_moving_average(data, tickerSymbol, startDate, endDate)
        elif(choice == "6"):
            dvl.moving_average_convergence_divergence(data, tickerSymbol, startDate, endDate)
        elif(choice == "7"):
            dvl.linear_trend_lines(data, tickerSymbol, startDate, endDate)
        else:
            print("Wrong choice. Please re-enter")
        choice = get_visualization_choice()
        
    
def export_data(tickerSymbol, startDate, endDate):
    data = yf.download(tickerSymbol, start = startDate, end = endDate)
    data.to_csv(tickerSymbol.lower() + '.csv')
    print(data)
    print(data.describe())
    