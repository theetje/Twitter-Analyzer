import tarfile
import bz2
import json

class TarFile(object):
    """docstring for [object Object]."""
    def __init__(self, root, name):
        self.tar = tarfile.open(root + "/" + name, 'r')

    def getTweets(self):
        """
        Geeft terug de tweets uit een gegeven input_file die in het bz2 format is.
        return json formatted tweets
        """
        tweets = []

        for file_name in self.tar.getnames():
            if file_name.endswith(".json.bz2"): # Kijk of het wel een .json.bz2 bestand is
                print("Current file: ", file_name)

                bz2_file = self.tar.extractfile(file_name)

                for line in bz2.open(bz2_file, 'rt'):
                    tweets.append(json.loads(line))

        return tweets
