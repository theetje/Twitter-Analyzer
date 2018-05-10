# -*- coding: utf-8 -*-
import json

class FileManager(object):
    """
    File Manager regeld alles wat nodig is om tweets uit de dataset te halen.
    """
    
    def getTweets(input_file):
        """geeft terug de tweets uit een gegeven input_file"""
        tweets = []

        for line in open(input_file, 'r'):
            tweets.append(json.loads(line))

        return tweets
