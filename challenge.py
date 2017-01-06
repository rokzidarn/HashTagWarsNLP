# SemEval 2017 Challenge - Task 6
# HashTagWars

#  --------------------------------------------------------------------------------
# imports
import re
import nltk
import numpy
import sklearn
import os
import string

#  --------------------------------------------------------------------------------
# classes
class Tweet:
    def __init__(self, id, hashtag, text, score, tokens):
        self.id = id
        self.hashtag = hashtag
        self.text = text
        self.score = score
        self.tokens = tokens

    def __str__(self):
        return 'TWEET ID: %d | HASHTAG: %s | TEXT: %s | SCORE: %d' % (self.id, self.hashtag, self.text, self.score)

    def tweetTokens(self):
        return self.tokens

# --------------------------------------------------------------------------------
# functions
def readFileByLineAndTokenize(file, subdirectory):
    tweets = [line.rstrip('\n') for line in open(subdirectory+file, 'r', encoding="utf8")]
    tokenized = [re.split('\s| ', tweet) for tweet in tweets]
    return tokenized

def filterText(text):  # remove unnecesary data from tweet, such as extra hashtags, links
    tweets = []
    for tweet in text:
        filtered = []
        for token in tweet:
            if(not(token.startswith('#') or token.startswith('@') or token.startswith('.@') or token.startswith('http'))):
                filtered.append(token)
        while filtered.__contains__(''):
            filtered.remove('')
        tweets.append(filtered)
        #print(filtered)
    return tweets

def createData(tweets, hashtag): # remove puncuation & stopwords, transform to lowercase, lemmas, create objects
    data = []
    for tweet in tweets:
        text = " ".join(tweet[1:-1]).lower()
        table = text.maketrans({key: None for key in string.punctuation})
        text = text.translate(table)

        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token not in nltk.corpus.stopwords.words('english')]
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(token) for token in tokens]

        obj = Tweet(int(tweet[0]), hashtag, text, int(tweet[-1]), lemmas)
        #print(obj)
        data.append(obj)
    return data

def printData(hashtagTweets):
    for j in range(len(hashtagTweets)):
        print(hashtagTweets[j])
        print("  TOKENS: " + str(hashtagTweets[j].tweetTokens()))

def getAllTokensFromHashtag(hashtagTweets):
    all = []
    for tweet in hashtagTweets:
        for token in tweet.tokens:
            all.append(token)
    return all

def getFunnyTweetsInHashtag(hashtagTweets): # score > 0
    funny = []
    for tweet in hashtagTweets:
        if tweet.score > 0:
            funny.append(tweet)
    return funny

def processTweets(hashtagTweets):  # basic data, frequency, important words
    print(hashtagTweets[0].hashtag)
    list = getAllTokensFromHashtag(hashtagTweets)
    freq = nltk.FreqDist(list)
    mostCommonWord = sorted(freq.items(), key = lambda x: x[1], reverse = True)[:2]
    print("Most common word: {}".format(mostCommonWord[0][0]))

    synset1 = nltk.corpus.wordnet.synsets(mostCommonWord[0][0])
    synset2 = nltk.corpus.wordnet.synsets(mostCommonWord[1][0])
    if (len(synset1) > 0 ):
        synonyms = []
        for lemma in synset1[0].lemmas():  # first synset only
            synonyms.append(lemma.name())
        print("Synonyms:  '{}'".format(set(synonyms)))
        #if(len(synset2) > 0):
            #print("2 most common words similarity: {} vs. {}: {:.2}".format(mostCommonWord[0][0], mostCommonWord[1][0],synset1[0].wup_similarity(synset2[0])))
    else:
        print("Synonyms:  /")

# --------------------------------------------------------------------------------
# main
dataList = [] # 2D list, [hashtag][tweet]
hashtags = [] # list of all hashtags
subdirectory = "test_data/"
for f in os.listdir(os.getcwd()+"/"+subdirectory):  # preprocessing
    hashtag = "#"+str(os.path.basename(f)[:-4].replace("_", ""))
    hashtags.append(hashtag)
    text = readFileByLineAndTokenize(f, subdirectory)
    tweets = filterText(text)
    hashtagList = createData(tweets, hashtag)
    dataList.append(hashtagList)

#for h in range(len(hashtags)):
    #hashtagTweets = dataList[h]
    #printData(hashtagTweets)

for i in range(len(dataList)):  # process each category (hashtag) separately
    hashtagTweets = dataList[i] # tweets from the same hashtag
    #processTweets(hashtagTweets)
    funnyTweets = getFunnyTweetsInHashtag(hashtagTweets)
    #printData(funnyTweets)
    processTweets(funnyTweets)
    print("-----------------------------")