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

from Classes.BColors import BColors
from Classes.TweetAnalyzer import TweetAnalyzer


def start():
    """Start the App"""
    """ Maak twee arrays met positive en negative worden. """
    negative_list = helpers.getWordsFromLexicons('sentiment-lexicons/negative-words.txt')
    positive_list = helpers.getWordsFromLexicons('sentiment-lexicons/positive-words.txt')

    top_dir = '/Volumes/Toshiba/Twitter-data/2017-11' # Locatie van de twitter data
    word_to_look_for = 'ibm' # woord waar je jaar gaat zoeken in underscore

    engine = create_engine('sqlite:///' + word_to_look_for + '.sqlite')
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


    for root, dirs, files in os.walk(top_dir, topdown=False): # Loop door de bestanden in test_data
        for name in files:
            print("Bezig met TarFile: ", name)

            if name.endswith(".tar"):
                tar = tarfile.open(root + "/" + name, 'r')
                for file_name in tar.getnames():
                    if file_name.endswith(".json.bz2"): # Kijk of het wel een .json.bz2 bestand is
                        print(file_name)
                        bz2_file = tar.extractfile(file_name)

                        for tweet in bz2.open(bz2_file, 'rt'):
                            json_tweet = json.loads(tweet)

                            if helpers.tweetConstraint(json_tweet, 'en', word_to_look_for) is not None:
                                tweet_sentiment = TweetAnalyzer.getSentiment(json_tweet,
                                                                            positive_list,
                                                                            negative_list)

                                for date, value in tweet_sentiment.items():
                                    newTweet = Tweet(text=json_tweet['text'],
                                                    positive_words=value['positive_words'],
                                                    negative_words=value['negative_words'],
                                                    date=date)
                                s = session()
                                s.add(newTweet)
                                s.commit()
