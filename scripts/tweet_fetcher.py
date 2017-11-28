from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import sys
import datetime

#Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '149028175-BwK3hB9maYaFcncQVkt0QR9Y84BVfdnNX5d2dhEh'
ACCESS_SECRET = 'B9Ysi3jQUstdWvV1MlqTx0fBmjV1d2hOxfW8014DEu3gH'
CONSUMER_KEY = 'F6YZ3q9nNTWHk02bsr0FqsMVK'
CONSUMER_SECRET = 'I57wNMA6hKdBcAqXJSeIgEIKK2A4nAymYfTZ6oP1v5UDEPqbmT'

def init():
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)

def check_if_user_exists(handle):
    try:
        twitter_accessor = init()
        twitter_accessor.user_timeline(handle)
        return True
    except:
        return False

def fetch_tweets_after_time(handle, since):
    twitter_accesser = init()
    # twitter_accesser.get_user(handle)
    startDate = since
    tweets = []
    tmpTweets = twitter_accesser.user_timeline(handle)
    for tweet in tmpTweets:
        if tweet.created_at > startDate:
            tweets.append(tweet)

    tweets_bk = []
    while (tmpTweets[-1].created_at > startDate):
        print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
        tmpTweets = twitter_accesser.user_timeline(handle, max_id=tmpTweets[-1].id)
        if tmpTweets == tweets_bk:
            break
        tweets_bk = tmpTweets
        for tweet in tmpTweets:
            if tweet.created_at > startDate:
                tweets.append(tweet)
    return tweets

# fetch_tweets_after_time("achillesHeelV2", "2016-06-01")
# print check_if_tweets_presents("achillesHeelV2xx")