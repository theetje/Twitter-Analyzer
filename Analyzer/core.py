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
    maxlag = 4
    plot_figure = False

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

    combined_results = helpers.combineRtandXt(Xt_dict, Rt_dict)

    result = sm.tsa.stattools.grangercausalitytests(combined_results, 4, addconst=True, verbose=True)
    exit()


    ln_Rt_dict = helpers.getRtDictFromCSV('2017/10/01',
                                        '2017/12/31',
                                        'data/stock/historical-quotes-'
                                        + word_to_analyze
                                        + '.csv')

    pos_neg_dict = helpers.getPositiveNegativePerDay(s, Tweet)

    pprint(pos_neg_dict)
    exit()
    Xt_dict = helpers.getXtnormalized(pos_neg_dict)
    combined_dicts = helpers.combineRtandXt(Xt_dict, Rt_dict)

    if plot_figure:
        Xt_df = pd.DataFrame(list(combined_dicts[0].items()), columns=['Date', 'Xt'])
        Xt_df['Date'] = pd.to_datetime(Xt_df['Date'])

        Rt_df = pd.DataFrame(list(combined_dicts[1].items()), columns=['Date', 'Rt'])
        Rt_df['Date'] = pd.to_datetime(Rt_df['Date'])

        Xt_df = Xt_df.sort_values('Date', ascending=True)
        plt.plot(Xt_df['Date'], Xt_df['Xt'])
        plt.xticks(rotation='horizontal')

        Rt_df = Rt_df.sort_values('Date', ascending=True)
        plt.plot(Rt_df['Date'], Rt_df['Rt'])
        plt.xticks(rotation='horizontal')

        plt.show()

    Xt_tuples = list(combined_dicts[0].items())
    Rt_tuples = list(combined_dicts[1].items())

    Xt_list = [x[1] for x in Xt_tuples]
    Rt_list = [r[1] for r in Rt_tuples]

    result = sm.tsa.stattools.grangercausalitytests([[Xt_list[i], Rt_list[i]] for i in range(0, len(Xt_list))], maxlag, addconst=True, verbose=True)
