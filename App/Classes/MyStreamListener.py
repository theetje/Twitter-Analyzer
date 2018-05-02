import tweepy

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if 'facebook' in status.text.lower():
            print(status.text)

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print('Timeout...')
        return True # Don't kill the stream

    # def on_status(self, status):
    #     print(status.text)
    #
    # def on_error(self, status_code):
    #     if status_code == 420:
    #         #returning False in on_error disconnects the stream
    #         return False
