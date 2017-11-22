#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys

#Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '149028175-BwK3hB9maYaFcncQVkt0QR9Y84BVfdnNX5d2dhEh'
ACCESS_SECRET = 'B9Ysi3jQUstdWvV1MlqTx0fBmjV1d2hOxfW8014DEu3gH'
CONSUMER_KEY = 'F6YZ3q9nNTWHk02bsr0FqsMVK'
CONSUMER_SECRET = 'I57wNMA6hKdBcAqXJSeIgEIKK2A4nAymYfTZ6oP1v5UDEPqbmT'


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        with open(sys.argv[1] + '_tweets.json', 'a') as tf:
            tf.write(data)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[sys.argv[1]], async=True)