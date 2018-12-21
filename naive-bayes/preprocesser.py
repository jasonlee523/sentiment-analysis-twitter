import re
import csv
from sys import argv

emoticons = \
	[	('__EMOT_SMILEY',	[':-)', ':)', '(:', '(-:', ] )	,\
		('__EMOT_LAUGH',		[':-D', ':D', 'X-D', 'XD', 'xD', ] )	,\
		('__EMOT_LOVE',		['<3', ':\*', ] )	,\
		('__EMOT_WINK',		[';-)', ';)', ';-D', ';D', '(;', '(-;', ] )	,\
		('__EMOT_FROWN',		[':-(', ':(', '(:', '(-:', ] )	,\
		('__EMOT_CRY',		[':,(', ':\'(', ':"(', ':(('] )	,\
	]
def escape_paren(arr):
	return [text.replace(')', '[)}\]]').replace('(', '[({\[]') for text in arr]

def regex_union(arr):
	return '(' + '|'.join( arr ) + ')'

emoticons_regex = [ (repl, re.compile(regex_union(escape_paren(regx))) ) \
					for (repl, regx) in emoticons ]

def processRow(row):
	tweet = row[0]
	#Lower case
	tweet.lower()
	#convert hashtags
	tweet = re.sub('#(\w+)', '__HASH_', tweet)
	#convert any url to URL
	tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
	#Convert any @Username to "AT_USER"
	tweet = re.sub('@[^\s]+','AT_USER',tweet)
	#Remove additional white spaces
	tweet = re.sub('[\s]+', ' ', tweet)
	tweet = re.sub('[\n]+', ' ', tweet)
	#Remove not alphanumeric symbols white spaces
	#tweet = re.sub(r'[^\w]', ' ', tweet)
	#Replace #word with word
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	#Replace Emoticons
	for (repl, regx) in emoticons_regex :
		tweet = re.sub(regx, ' '+repl+' ', tweet)
	#trim
	tweet = tweet.strip('\'"')

	row[0] = tweet

	return row


if __name__ == '__main__':
    #Read the tweets one by one and process it
    pos_file = open('positive_tweets_.csv','wb')
    filewriter_pos = csv.DictWriter(pos_file, fieldnames=["Text", "Sentiment"])

    with open('training.1600000.processed.noemoticon.csv.5000.norm.csv', "rb") as csvfile:
        filereader = csv.reader(csvfile)
        for row in filereader:
            new_row = processRow(row)
            if(row[1] == 'pos'):
                filewriter_pos.writerow({
                "Text" : new_row[0],
                "Sentiment" : new_row[1]
                })
        pos_file.close()

    neg_file = open('negative_tweets_.csv','wb')
    filewriter_neg = csv.DictWriter(neg_file, fieldnames=["Text", "Sentiment"])

    with open('training.1600000.processed.noemoticon.csv.5000.norm.csv', "rb") as csvfile:
        filereader_ = csv.reader(csvfile)
        for row in filereader_:
            new_row = processRow(row)
            if(row[1] == 'neg'):
                filewriter_neg.writerow({
                "Text" : new_row[0],
                "Sentiment" : new_row[1]
                })
        neg_file.close()
