import json
import csv
topics = ["Politics", "Sports", "Business", "Science", "Lifestyle", "Philosophy", "Economics"]
topic_tweet_count = {}
with open("datasets.tsv", "w") as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    writer.writerow(["Tweet", "Label"])
    for topic in topics:
        lineCount = 0
        topic_tweets = open(topic + "_tweets.json")
        for line in topic_tweets:
            tweet = json.loads(line.strip())
            if "text" not in tweet.keys() or tweet["lang"] != "en":
                continue
            lineCount = lineCount + 1
            writer.writerow([unicode(tweet["text"]).encode("utf-8"), topic])
        topic_tweet_count[topic] = lineCount
for key, value in topic_tweet_count.items():
    print key + "\t" + str(value)
