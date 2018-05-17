# -*- coding: utf-8 -*-
import helpers
import json
import os
# import tarfile
# import bz2
import string

from pprint import pprint
# from pathlib import Path
# from Classes.FileManager import FileManager
from Classes.BColors import BColors
from Classes.TweetAnalyzer import TweetAnalyzer

from Models.TarFile import TarFile

def start():
    """Start the App"""
    """ Maak twee arrays met positive en negative worden. """
    negative_list = helpers.getWordsFromLexicons('sentiment-lexicons/negative-words.txt')
    positive_list = helpers.getWordsFromLexicons('sentiment-lexicons/positive-words.txt')

    top_dir = 'test_data' # Locatie van de twitter data

    for root, dirs, files in os.walk(top_dir, topdown=False): # Loop door de bestanden in test_data
        for name in files:
            if name.endswith(".tar"):
                tarFile = TarFile(root, name) # Maak een taar file object

                tweets = tarFile.getTweets()
                for tweet in tweets: # Loop door te tweets
                    # First arg is tweet 2nd arg is language thrd arg is for the subject
                    analyzable_tweet = helpers.tweetConstraint(tweet, 'en', 'facebook')
                    if analyzable_tweet is not None:

                        tweet_sentiment = TweetAnalyzer.getSentiment(analyzable_tweet, positive_list, negative_list)
                        for date, value in tweet_sentiment.items():
                            # helpers.saveTweet('results/json_result.json', ) TODO ga verder met deze functie
                            with open('results/json_result.json', 'r') as f: # Open de bestaande uitkomsten
                                json_data = json.load(f)

                                if date in json_data:
                                    json_data[date]["positive_words"] += value['positive_words']
                                    json_data[date]["negative_words"] += value['negative_words']
                                else:
                                    json_data.update(tweet_sentiment)

                            with open('results/json_result.json', 'w') as fp: # Schrijf de uitkomsten opnieuw weg
                                json.dump(json_data, fp)
