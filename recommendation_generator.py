from scripts.tweet_fetcher import fetch_tweets_after_time
import sys
from services.src.db_helper import DbHelper
from services.src.db_helper import Tweet
import scripts.classifier
import datetime

def generate_recommendations(twitter_handle):
    helper = DbHelper()
    user_id, last_tweet_timestamp = helper.get_last_tweet_timestamp(handle=twitter_handle)
    if last_tweet_timestamp is None:
        last_tweet_timestamp = datetime.datetime.strptime("2016-01-01", "%Y-%m-%d")
    tweets = fetch_tweets_after_time(twitter_handle, last_tweet_timestamp)
    if not tweets:
        print "No tweets available yet"
        return
    tweet_text_list = [(tweet.text, tweet.id) for tweet in tweets]
    classified_tweets = scripts.classifier.classify_tweets(tweet_text_list)
    print classified_tweets
    labeled_tweets = []
    for tweet in tweets:
        db_tweet = Tweet(tweet.text, classified_tweets[tweet.id][0], tweet.created_at, user_id, classified_tweets[tweet.id][1].item())
        labeled_tweets.append(db_tweet)
    helper.insert_all_tweets(labeled_tweets)
    score = helper.get_user_affinity_score(user_id)
    helper.insert_update_affinity_scores(user_id, score)
    helper.update_db_interests(user_id)

#print generate_recommendations("achillesHeelV2")
# helper = DbHelper()
# helper.update_db_interests(1)