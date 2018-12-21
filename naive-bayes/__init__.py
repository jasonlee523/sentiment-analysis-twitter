
FULLDATA = 'training.1600000.processed.noemoticon.csv'
TESTDATA = 'testdata.manual.2009.06.14.csv'

POLARITY= 0 # in [0,5]
TWID    = 1
DATE    = 2
SUBJ    = 3 # NO_QUERY
USER    = 4
TEXT    = 5

import csv, re, random

regex = re.compile( r'\w+|\".*?\"' )

def get_class( polarity ):
    if polarity in ['0', '1']:
        return 'neg'
    elif polarity in ['3', '4']:
        return 'pos'
    elif polarity == '2':
        return 'neu'
    else:
        return 'err'

def get_query( subject ):
    if subject == 'NO_QUERY':
        return []
    else:
        return regex.findall(subject)

def getAllQueries(in_file):
    fp = open(in_file , 'r')
    rd = csv.reader(fp, delimiter=',', quotechar='"' )
    queries = set([])

    for row in rd:
        queries.add(row[3])

    return queries

def randomSampleCSV( in_file, out_file, K=100 ):
    fp = open(in_file , 'r')
    fq = open(out_file, 'w')
    rows = [None] * K

    i = 0
    for row in fp:
        i+=1
        j = random.randint(1,i)
        if i < K:
            rows[i] = row
        elif j <= K:
            rows[j-1] = row

    for row in rows:
        fq.write(row)

    min(1, K/i)

def getNormalisedCSV( in_file, out_file ):
    fp = open(in_file , 'r')
    rd = csv.reader(fp, delimiter=',', quotechar='"' )
    fq = open(out_file, 'w')
    wr = csv.writer(fq, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL )

    for row in rd:
        queries = get_query(row[SUBJ])
        wr.writerow( [row[TEXT], get_class(row[POLARITY]), row[SUBJ]] + [len(queries)] + queries )

getAllQueries( 'training.1600000.processed.noemoticon.csv' )

randomSampleCSV(FULLDATA, FULLDATA+'.5000.sample.csv', K=5000)
getNormalisedCSV(FULLDATA+'.5000.sample.csv', FULLDATA+'.5000.norm.csv')
