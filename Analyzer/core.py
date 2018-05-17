# -*- coding: utf-8 -*-
import helpers
import json
import os
import tarfile
import bz2
import string

from pprint import pprint

from Models.base import Base
from Models.Tweet import Tweet

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def start():
    """Start the Data Analyzer"""

    top_dir = 'test_data' # Locatie van de twitter data
    word_to_look_for = 'ibm' # woord waar je jaar gaat zoeken in underscore

    engine = create_engine('sqlite:///' + word_to_look_for + '.sqlite')
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()

    for date, text in s.query(Tweet.date, Tweet.text):
        print("On " + str(date) + " the following was tweeted: ")
        print(text)
