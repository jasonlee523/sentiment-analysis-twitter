from sys import argv
from sys import exit

import csv

import preprocesser
import feature_extractor
import nltk

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk import metrics
from nltk.metrics import precision
import collections
print(dir(nltk))

script,  tweets_, stop_words_file_name = argv
word_features = []

def read_tweets(tweet_file):

    features = []
    tweets = []

    with open(tweet_file,'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for l in csv_reader:
            new_row = preprocesser.processRow(l)
            features = feature_extractor.getFeatureVector(new_row[0], stop_words_file_name)
            tweets.append(
            ( [f.strip("\'") for f in features],
            new_row[1]
            ))
    return tweets

def extract_features(document):

	document_words = set(document)
	features = {}
	for w in word_features:
		features['contains %s'% w] = (w in document_words)
	return features

if __name__ == '__main__':
    negtweets = []
    postweets = []

    fp = open(tweets_, 'r')
    rd = csv.reader(fp, delimiter=',', quotechar='"' )

    fq = open('positive_tweets_.csv', 'w')
    wr = csv.writer(fq, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL )
    for row in rd:
        if(row[1] == 'pos'):
            wr.writerow( [row[0], row[1]])
    fq.close()
    fp.close()

    fp_ = open(tweets_, 'r')
    fw = open('negative_tweets_.csv', 'w')
    rd_ = csv.reader(fp_, delimiter=',', quotechar='"' )
    wr_ = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL )
    for row in rd_:
        if(row[1] == 'neg'):
            wr_.writerow( [row[0], row[1]])
    fw.close()

    neg_tweets = read_tweets('negative_tweets_.csv')
    pos_tweets = read_tweets('positive_tweets_.csv')
    cutoff = 0

    if(len(neg_tweets) > len(pos_tweets)):
        cutoff = len(pos_tweets)*4/5
    else:
        cutoff = len(neg_tweets)*4/5

    tweets = neg_tweets[:cutoff] + pos_tweets[:cutoff]
    test_tweets = neg_tweets[cutoff:] + pos_tweets[cutoff:]
    all_words = []
    words_frequency = []
    print(tweets)
    #Get all the words
    for (words, sentiment) in tweets:
        all_words.extend(words)

    #extract the features
    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()
    training_set = nltk.classify.apply_features(extract_features, tweets)
    classifier = NaiveBayesClassifier.train(training_set)
    refsets  = { 'pos': set([]), 'neg':set([])}
    testsets = { 'pos': set([]), 'neg':set([])}

    classifier.show_most_informative_features()

    for i, (feats, label) in enumerate(test_tweets):
        refsets.get(label).add(i)
        testsets[classifier.classify(extract_features(feats))].add(i)

    print('pos precision:', nltk.precision(refsets['pos'], testsets['pos']))
    print('pos recall:', nltk.recall(refsets['pos'], testsets['pos']))
    print('pos F-measure:', nltk.f_measure(refsets['pos'], testsets['pos']))
    print('neg precision:', nltk.precision(refsets['neg'], testsets['neg']))
    print('neg recall:', nltk.recall(refsets['neg'], testsets['neg']))
    print('neg F-measure:', nltk.f_measure(refsets['neg'], testsets['neg']))
