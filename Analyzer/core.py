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
from statsmodels.tsa.api import VAR, DynamicVAR

from settings import *

def start():
    """Start the Data Analyzer"""
    engine = create_engine('sqlite:///' + word_to_analyze + '.sqlite')
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()

    if count_rows:
        print("Number of tweets used from " + word_to_analyze + ": ")
        print(helpers.countRows(s, Tweet))

    log_Xt_dict = helpers.getXFromData(s, Tweet, True)
    log_Rt_dict = helpers.getRFromCSV('2017/10/01',
                                        '2017/12/31',
                                        'data/stock/'
                                        + word_to_analyze
                                        + '-stock-data'
                                        + '.csv',
                                        True)

    combined_2d_results_log = helpers.combineRtandXt(log_Xt_dict, log_Rt_dict)

    # VAR
    if test_var:
        pd_data = pd.DataFrame(combined_2d_results_log, columns=['Xt', 'Rt'])
        var_result = VAR(pd_data).fit(maxlag)

        print(var_result.summary())
        var_result.test_causality('Rt', 'Xt')

        # VOORBEELD VAN HOE BESCHRIJVENDE STATESTIEK KAN WORDEN GEPLOT:
        # fig = plt.subplots()
        # fig = var_result.plot_sample_acorr()
        # ax.set_ylabel("Y lable")
        # ax.set_xlabel("X lable")
        # ax.set_title("Title")
        # plt.show()

    # GRANGER CAUSALITY ANALYSIS
    if test_granger:
        result = sm.tsa.stattools.grangercausalitytests(combined_2d_results_log,
                                                        maxlag,
                                                        addconst=True,
                                                        verbose=True)

    # PLOT DATA
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
