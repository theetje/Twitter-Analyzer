# -*- coding: utf-8 -*-
import json
import bz2
import tarfile

class FileManager(object):
    """
    File Manager regeld alles wat nodig is om tweets uit de dataset te halen.
    """
    def getTweets(file_name, tar):
        """
        Geeft terug de tweets uit een gegeven input_file die in het bz2 format is.
        """
        tweets = []
        bz2_file = tar.extractfile(file_name)

        for line in bz2.open(bz2_file, 'rt'):
            tweets.append(json.loads(line))

        return tweets
