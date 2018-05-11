from datetime import datetime

class TweetAnalyzer(object):
    """docstring for [object Object]."""

    """ Geef de datem terug vanuit een ms time. """
    def getDateFromMSTime(timestamp_ms):
        s = int(timestamp_ms) / 1000.0
        return datetime.fromtimestamp(s).strftime('%Y-%m-%d')

    """ Geef het sentiment van een tweet terug als een dict. """
    def getSentiment(tweet, positive_list, negative_list):
        words_in_tweet = tweet['text'].split() # Stop de worden in een list

        date = TweetAnalyzer.getDateFromMSTime(tweet['timestamp_ms'])
        positive_words = len(set(words_in_tweet) & set(positive_list))
        negative_words = len(set(words_in_tweet) & set(negative_list))

        return {date : { "positive_words" : positive_words,
                         "negative_words" : negative_words }}
