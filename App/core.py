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


    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    #
    # for status in tweepy.Cursor(api.home_timeline).items(100):
    #     # Process a single status
    #     print(status.text)

    myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    # myStream.filter(track=['facebook'])

    sapi = tweepy.streaming.Stream(auth, listener=myStreamListener)
    sapi.filter(languages=["en"], track=["a", "the", "i", "you", "u", "it", "for", "do", "in"])
