# -*- coding: utf-8 -*-
import helpers
import json
import os
import tarfile
import bz2

from pprint import pprint
# from pathlib import Path
from Classes.FileManager import FileManager
from Classes.BColors import BColors
from Classes.TweetAnalyzer import TweetAnalyzer

def start():
    """Start the App"""
    """ Maak twee arrays met positive en negative worden. """
    negative_list = helpers.getWordsFromLexicons('sentiment-lexicons/negative-words.txt')
    positive_list = helpers.getWordsFromLexicons('sentiment-lexicons/positive-words.txt')

    top_dir = 'test_data' # Locatie van de twitter data

    for root, dirs, files in os.walk(top_dir, topdown=False): # Loop door de bestanden in test_data
        for name in files:
            if name.endswith(".tar"):
                tar = tarfile.open(root + "/" + name, 'r')
                file_names = tar.getnames()

                for file_name in file_names:
                    if file_name.endswith(".json.bz2"): # Kijk of het wel een .json.bz2 bestand is
                        tweets = FileManager.getTweets(file_name, tar)

                        for tweet in tweets: # Loop door te tweets
                            if 'lang' in tweet: # Kijk of in de tweet de taal word aangegeven
                                if tweet['lang'] == 'en': # Kijk of de taal in de tweet engels is
                                    tweet_sentiment = TweetAnalyzer.getSentiment(tweet, positive_list, negative_list)

                                    for date, value in tweet_sentiment.items():
                                        with open('results/json_result.json', 'r') as f: # Open de bestaande uitkomsten
                                            json_data = json.load(f)

                                            if date in json_data:
                                                json_data[date]["positive_words"] += value['positive_words']
                                                json_data[date]["negative_words"] += value['negative_words']
                                            else:
                                                json_data.update(tweet_sentiment)

                                        with open('results/json_result.json', 'w') as fp: # Schrijf de uitkomsten opnieuw weg
                                            json.dump(json_data, fp)
