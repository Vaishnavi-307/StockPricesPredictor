# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 21:55:32 2020

@author: hp
"""
import yfinance as yf
import pandas as pd 
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from scipy.stats import sem, t
import DataVisualizationLogic as dvl
                                                                                                                                                                                                                                                                                                                        
def stock_prediction(tickerSymbol, duration):
    ticker=yf.Ticker(tickerSymbol)
    df=ticker.history(period=duration)
    if(duration!='1d' and len(df)>2):
        df.index = (df.index - pd.to_datetime('1970-01-01')).days   #converting dates to integer values by subtracting from 1970-01-01
        y = np.asarray(df['Close'])
        x = np.asarray(df.index.values)
        regression_model = LinearRegression()   #using the linear regression model for prediction
    
        regression_model.fit(x.reshape(-1, 1), y.reshape(-1, 1))
        y_learned = regression_model.predict(x.reshape(-1, 1))
        days=input('Enter number of days for which you want to predict the closing price: ')
        if(days.isdigit()):
            newindex = np.asarray(pd.RangeIndex(start=x[-1], stop=x[-1] + int(days)))
            y_predict = regression_model.predict(newindex.reshape(-1, 1))
            #converting back to dates from integers
            x = pd.to_datetime(df.index, origin='1970-01-01', unit='D') 
            future_x = pd.to_datetime(newindex, origin='1970-01-01', unit='D')
            
            future_xdf = pd.DataFrame(future_x)
            y_predictdf = pd.DataFrame(y_predict)
            df.to_csv(tickerSymbol.upper() + '_Prediction.csv')
            future_xdf.to_csv(tickerSymbol.upper() + '_Prediction.csv', header = "Date")
            y_predictdf.to_csv(tickerSymbol.upper() + '_Prediction.csv', mode = 'a', header = "Prices")
            print("Future Dates:\n", future_x)
            print("Stock Prices: \n", y_predict)
        
            #plot the regression model
            plt.plot(x,y_learned, color='r', label='Linear Model')
        
            #plot the future predictions
            #plt.figure(figsize=(14,7))
            plt.plot(future_x,y_predict, color='g', label='Future prediction')
            plt.plot(x,df['Close'], label='Close Price History')
        
            plt.suptitle('Stock Market Predictions for ' + tickerSymbol.upper(), fontsize=16)
            plt.xlabel('Date')
            plt.ylabel('Closing Price')
        
            fig = plt.gcf()
            fig.canvas.set_window_title('Close Price Predictions')
            fig.autofmt_xdate()
        
            plt.legend()
            dvl.download_plot(tickerSymbol.upper() + '_LinearRegression.png')
            plt.show()
                      
            
