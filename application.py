from sys import argv
from sys import exit

import nltk
import csv
import tweets
import os, sys
from analyzer import Analyzer

def search():
    negTweets = []
    posTweets = []

    with open('positiveTweets.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for l in csv_reader:
            posTweets.append([l[0], l[1]])
        #tweets_ = tweets.tweets

    with open('negativeTweets.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for l in csv_reader:
            negTweets.append([l[0], l[1]])
        #tweets_ = tweets.tweets

    # load absolute path of word lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)
    positive, negative, neutral = 0.0, 0.0, 0.0

    cutoff = 0
    if(len(negTweets) > len(posTweets)):
        cutoff = len(posTweets)*4/5
    else:
        cutoff = len(negTweets)*4/5

    tweets_ = negTweets[:cutoff] + posTweets[:cutoff]
    testTweets_ = negTweets[cutoff:] + posTweets[cutoff:]
    refsets  = { 'pos': set([]), 'neg':set([])}
    testsets = { 'pos': set([]), 'neg':set([])}

    for tweet in tweets_:
        score = analyzer.analyze(tweet[0])
        if tweet[1]=='pos':
            testsets['pos'].add(tweet[0])
        else:
            testsets['neg'].add(tweet[0])
        if score > 0.0:
            positive += 1.0
            refsets['pos'].add(tweet[0])
        elif score <= 0.0:
            negative += 1.0
            refsets['neg'].add(tweet[0])
        else:
            neutral += 1.0

    print('pos precision:', nltk.precision(refsets['pos'], testsets['pos']))
    print('pos recall:', nltk.recall(refsets['pos'], testsets['pos']))
    print('pos F-measure:', nltk.f_measure(refsets['pos'], testsets['pos']))
    print('neg precision:', nltk.precision(refsets['neg'], testsets['neg']))
    print('neg recall:', nltk.recall(refsets['neg'], testsets['neg']))
    print('neg F-measure:', nltk.f_measure(refsets['neg'], testsets['neg']))

    print(str(positive)+','+str(negative))

search()
