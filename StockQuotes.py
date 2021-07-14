# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 02:31:45 2020

@author: hp
"""
#import libraries
import pandas as pd
import StockPredictorLogic as spl
import DataVisualizationMenu as dvm
import yfinance as yf
import datetime as dt

def display_welcome():
    print("Welcome to the main menu of Vaishnavi's Stock Application! \nThe following are your options:")   

def get_choice():  
    #display menu options
    print("\nMain Menu \n1. Search Stocks\n2. Query Time Range\n3. Data Visualization ",
          "\n4. Stock Market Prediction \n5. Display Descriptive Analytics on console and Download Data to CSV file",
          "\n6. Terms and Conditions \n0. Quit")
    return input("Please choose an option (0 to exit): ")

def get_ticker_and_date():
    """let the user enter the ticker data"""
    tickerSymbol = input("Please choose ticker symbol: ")
    startDate = input("Please input the start date (YYYY-MM-DD): ")
    endDate = input("Please input the end date (YYYY-MM-DD): ")
    
    #check for valid input of ticker symbol and date range
    date_format = '%Y-%m-%d'
    try:
        startDate = dt.datetime.strptime(startDate, date_format)
        endDate = dt.datetime.strptime(endDate, date_format)
        if (endDate >= startDate and dt.datetime.now() >= endDate and dt.datetime.now() >= startDate):
            info_ticker = yf.Ticker(tickerSymbol)
            info_ticker.info['longName']
            return (tickerSymbol, startDate, endDate)
        else:
            print("End date value should be '>=' the Start date value.\n Kindly enter the correct values.")
            return get_ticker_and_date()
    except Exception as e:
        print (e)
        if (str(e) == "'regularMarketOpen'"):
            print('Oops! You entered a invalid Ticker symbol. Please re-enter.')
        else:
            print("Invalid date range! Please enter the correct date value!",e)
        input_flag = 1
        if (input_flag == 1):
            return get_ticker_and_date()
        return tickerSymbol, startDate, endDate

#read the CSV file
def retrieve_companylist():
    return pd.read_csv('companylist.csv')

#search the stocks
def search_stocks(company_list):
    print('Search Stocks')
    symbol = input("Please choose ticker symbol: ")
    filtered_companies = company_list[
        (company_list.Symbol.str.lower().str.contains(symbol.lower()))
                | (company_list.Name.str.lower().str.contains(symbol.lower()))]
    print(filtered_companies)
    print(filtered_companies.describe())
    
    
#search the stocks based on the ticker symbol and data period
def query_time_range():
    tickerSymbol, duration = get_ticker_and_duration()
    # tickerSymbol = input("Please enter a ticker symbol: ")
    # duration = input("Please enter period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
    data = None
    while data is None:
        try:
            tickerInfo = yf.Ticker(tickerSymbol)
            if(duration not in ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]):
               print("Enter a valid duration period!")
               return query_time_range()
            print(tickerInfo)
            history = tickerInfo.history(period = duration)
            print(history)
            
        except Exception as e:
            print (e)
            if (str(e) == "'regularMarketOpen'"):
                print("Oops! You entered a invalid Ticker symbol. Please re-enter.")
            input_flag = 1
            if (input_flag == 1):
                return query_time_range()
        return tickerSymbol, duration
            
#get the ticker and data period from the user. Reuse this function whenever needed    
def get_ticker_and_duration():
    tickerSymbol = input("Please choose ticker symbol: ")
    duration = input("Please enter period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
    return tickerSymbol, duration

#download the data from YFinance
def download_data(tickerSymbol, startDate, endDate):
    data = yf.download(tickerSymbol, start = startDate, end = endDate)
    return data

#the choice function is called here
def data_visualization():
    print("\nWelcome to the Data Visualization Sub-menu! \n")
    print("Let's take the parameters (Ticker Symbol, Start Date and End Date, so you can",
          "view different type of plots for these specific parameters \n")
    tickerSymbol, startDate, endDate = get_ticker_and_date()
    dvm.visualization_menu()
    choice = dvm.get_visualization_choice()
    data = download_data(tickerSymbol, startDate, endDate)
    dvm.process_choice(choice, data, tickerSymbol, startDate, endDate)

#predictive analysis function is called here
def predictive_analysis():
    tickerSymbol, duration = get_ticker_and_duration()
    spl.stock_prediction(tickerSymbol, duration)

#export the downloaded data to CSV file    
def export_data(tickerSymbol, startDate, endDate):
    data = yf.download(tickerSymbol, start = startDate, end = endDate)
    print("The downloaded data is: \n", data)
    print("Descriptive statistics for data is: ", data.describe())
    data.to_csv(tickerSymbol.lower() + '.csv')
    data.describe().to_csv(tickerSymbol.lower() + '.csv', mode = 'a', header = False)

#terms and conditions are read from text file
def terms_and_conditions():
    for line in open("TermsAndConditions.txt"):
        print(line, end = "")

#process the user's choice 
def process_choice(choice, company_list):
    while choice!="0":
        if(choice=="1"):
            search_stocks(company_list)
        elif(choice=="2"):
            #tickerSymbol, duration = get_ticker_and_duration()
            query_time_range()
        elif(choice=="3"):
            data_visualization()
        elif(choice=="4"):
            predictive_analysis()
        elif(choice == "5"):
            print("Let's take parameters to download the data in CSV format along with descriptive statistics.")
            tickerSymbol, startDate, endDate = get_ticker_and_date()
            export_data(tickerSymbol, startDate, endDate)
        elif(choice=="6"):
            terms_and_conditions()
        else:
            print("Wrong choice. Please try again")
        choice = get_choice()

#initialize the application. Starting point
def main():
    company_list = retrieve_companylist()
    display_welcome()
    choice = get_choice()
    process_choice(choice, company_list)

if __name__ == '__main__':
    main()
