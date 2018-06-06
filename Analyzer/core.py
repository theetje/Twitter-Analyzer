# -*- coding: utf-8 -*-
# helpers
import csv
import helpers
from pprint import pprint

# models
from Models.base import Base
from Models.Tweet import Tweet

# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# statsmodels numpy, matplotlib and pandas for analysis
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def start():
    """Start the Data Analyzer"""

    word_to_analyze = 'ibm' # de database naam
    maxlag = 4 # amount of lag days used
    plot_figure = False # plot the Xt and Rt results
    count_rows = True # count the amount of rows from the database

    engine = create_engine('sqlite:///' + word_to_analyze + '.sqlite')
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()

    # Get the delta X sentiment score per day
    Xt_dict = helpers.getXFromData(s, Tweet)
    # Get the Return on stock for a given period from the dataset
    Rt_dict = helpers.getRFromCSV('2017/10/01',
                                        '2017/12/31',
                                        'data/stock/historical-quotes-'
                                        + word_to_analyze
                                        + '.csv')

    if count_rows:
        print("Number of tweets used from " + word_to_analyze + ": ")
        print(helpers.countRows(s, Tweet))

    combined_results = helpers.combineRtandXt(Xt_dict, Rt_dict)

    result = sm.tsa.stattools.grangercausalitytests(combined_results, maxlag, addconst=True, verbose=True)

    if plot_figure:
        Xt_df = pd.DataFrame(list(Xt_dict.items()), columns=['Date', 'Xt'])
        Xt_df['Date'] = pd.to_datetime(Xt_df['Date'])

        Rt_df = pd.DataFrame(list(Rt_dict.items()), columns=['Date', 'Rt'])
        Rt_df['Date'] = pd.to_datetime(Rt_df['Date'])

        Xt_df = Xt_df.sort_values('Date', ascending=True)
        plt.plot(Xt_df['Date'], Xt_df['Xt'])
        plt.xticks(rotation='horizontal')

        Rt_df = Rt_df.sort_values('Date', ascending=True)
        plt.plot(Rt_df['Date'], Rt_df['Rt'])
        plt.xticks(rotation='horizontal')

        plt.show()
