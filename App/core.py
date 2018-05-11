# -*- coding: utf-8 -*-
import helpers
import json

from pprint import pprint
from Classes.FileManager import FileManager
from Classes.BColors import BColors
from Classes.TweetAnalyzer import TweetAnalyzer

def start():
    """Start the App"""
    """ Maak twee arrays met positive en negative worden. """
    negative_list = helpers.getWordsFromLexicons('sentiment_lexicons/negative-words.txt')
    positive_list = helpers.getWordsFromLexicons('sentiment_lexicons/positive-words.txt')

    tweets = FileManager.getTweets('test_data/30.json')

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
                            json_data  = tweet_sentiment

                    with open('results/json_result.json', 'w') as fp: # Schrijf de uitkomsten opnieuw weg
                        json.dump(json_data, fp)
