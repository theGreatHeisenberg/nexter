import re
from nltk.corpus import stopwords

def get_clean_tweet(tweet):
    tweet_without_links = re.sub(r"http\S+", "", tweet)
    words = re.findall(r'\w+', tweet_without_links, flags=re.UNICODE | re.LOCALE)
    return " ".join(filter(lambda tweet: tweet not in stopwords.words('english'), words))

# print get_cleaned_tweet("@swiggy_in  : https://t.co/pEyfq4nqL9 is not working. Is it down? or hacked by Turkish hackers?")