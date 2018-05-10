# -*- coding: utf-8 -*-
import helpers
import re

from pprint import pprint

from Classes.FileManager import FileManager
from Classes.BColors import BColors

def start():
    """Start the App"""
    """ Maak twee arrays met positive en negative worden. s"""
    # negative_array = helpers.getWordsFromLexicons('sentiment_lexicons/negative-words.txt')
    # positive_array = helpers.getWordsFromLexicons('sentiment_lexicons/positive-words.txt')


    # tweets = FileManager.getTweets('test_data/30.json')
    #
    # for tweet in tweets: # Loop door te tweets
    #     if 'lang' in tweet: # Kijk of in de tweet de taal word aangegeven
    #         if tweet['lang'] == 'en':
    #             print(tweet['text'])
    #     else: # Kijk of er tweets zijn die geen lang hebben en print in oranje.
    #         if 'text' in tweet:
    #             print(BColors.WARNING + tweet['text'] + BColors.ENDC)
