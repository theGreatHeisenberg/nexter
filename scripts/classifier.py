# coding: utf-8
import pandas
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

import text_processor

def classify_tweets(tweets):
    data = pandas.read_csv(open("/home/shreyas/Downloads/datasets.tsv"), sep="\t")
    # data = pandas.read_csv(open("/home/shreyas/datasets.tsv"), sep="\t")
    target = data["Label"]
    # count_vect = CountVectorizer(stop_words="english", ngram_range=(1,2))
    count_vect = CountVectorizer(stop_words="english")
    X_train_counts = count_vect.fit_transform(data.Tweet)
    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    X_train_tf.shape
    clf = SGDClassifier(loss='log', penalty='l2',alpha=1e-2, random_state=42,max_iter=3, tol=None).fit(X_train_tf, target)
    # clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True).fit(X_train_tf, target)
    # clf = SVC(probability=True).fit(X_train_tf, target)
    docs_modified = [text_processor.get_clean_tweet(tweet) for tweet,id in tweets]
    ids = [id for tweet,id in tweets]
    X_new_counts = count_vect.transform(docs_modified)
    X_new_tfidf = tf_transformer.transform(X_new_counts)
    predicted = clf.predict_proba(X_new_tfidf)
    out = {}
    for id, doc, predicted in zip(ids, docs_modified, predicted):
        max_prob = 0
        label = None
        for classname, probability in zip(clf.classes_, predicted):
            if (probability >= max_prob):
                max_prob = probability
                label = classname
        out[id] = (label, max_prob)
    return out
# print classify_tweets([("There are only 2 hard things in Computer Science: cache invalidation, naming things and off-by-one error. #programming","asd")])