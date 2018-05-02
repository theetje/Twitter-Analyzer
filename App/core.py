# -*- coding: utf-8 -*-

import helpers
import tweepy

from tweepy import OAuthHandler
from Classes.MyStreamListener import MyStreamListener

def start():
    """Start the App"""
    consumer_key = 	'8xKeKjwFOFbHvokkC6bErIdjC'
    consumer_secret = '6o0mAvdNo8ek7aTmhLDYW0wPs63qtiBzavjG7jPBOcYRxc3Lyi'
    access_token = '113985938-hWty1EeAIFYSZICt91OtKCOMgsk02htVyiVRak9A'
    access_secret = 'RJunHQkelx2mBEQnsXQshLAbP3omE93zXzNNgYDx2O1jB'

    """
    Auth die gebruikt woord door de twitter api zoals bedoeld is door tweepy
    """
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    """ Stream listener object met filters. """
    myStreamListener = MyStreamListener()

    """ Track list van woorden die engels definieren. """
    track_list = ["a", "the", "i", "you", "u", "it", "for", "do", "in"]

    stream = tweepy.streaming.Stream(auth, listener=myStreamListener)
    stream.filter(languages=["en"], track=track_list)
