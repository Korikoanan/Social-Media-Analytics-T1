# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:28:16 2022

@author: user
"""
import tweepy
from textblob import TextBlob
import re
import string
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist, bigrams


def twitter_setup():
    #Authentication and access using keys
    consumer_key = "3tb2uKZTbOa78pKtN9lFWh2mt"
    consumer_secret = "1a8yR9kMAEfc8DSGHbuzXi1cxzdI8BSWXPhCOTQOirUXu5xiE6"
    access_key = "823864824727646209-wjU9Kw8kRWNhwzVK5tOUgWQWTdFcaKF"
    access_secret = "LQqYO9PofZ9uytCHbz5nkmT31pzRRwBBC2O0KNwA103fP"
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return api 
extractor = twitter_setup()
def keyword_tweets(api, keyword, number_of_tweets):
    new_keyword = keyword + "-filter:retweets"
    
    tweets=[]
    for status in tweepy.Cursor(api.search_tweets, q=new_keyword, lang="en").items(number_of_tweets):
        tweets.append(status)
    return tweets

keyword_alltweets = keyword_tweets(extractor, "Xiaomi", 10)
data = pd.DataFrame(data=[tweet.text for tweet in keyword_alltweets], columns=['Tweets'])
data.to_csv("C:/Users/user/Documents/Social Media Analytics/tweets.csv")

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos= 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos= 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word,pos))
    return lemmatized_sentence
def remove_noise(tweet_tokens, stop_words):
        cleaned_tokens = []
        for token in tweet_tokens:
            token = re.sub('http[s]','',token)
            token = re.sub('//t.co[A-Za=z0-9]+','',token)
            token = re.sub('(@[A-Za-z0-9_]+)','',token)
            if(len(token) > 3) and (token not in string.punctuation) and (token.lower() not in stop_words):
                cleaned_tokens.append(token.lower())
        return cleaned_tokens
stop_words = stopwords.words('english')
stop_words.extend (['XiaoMi','Feedback','Customer'])

tweets_token=data['Tweets'].apply(word_tokenize).tolist()

cleaned_tokens = []
for tokens in tweets_token:
    rm_noise=remove_noise(tokens, stop_words)
    lemma_tokens=lemmatize_sentence(rm_noise)
    cleaned_tokens.append(lemma_tokens)
def get_all_words(cleaned_tokens_list):
    tokens=[]
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token
tokens_flat=get_all_words(cleaned_tokens)
freq_dist = FreqDist(tokens_flat)
print(freq_dist.most_common(20))

bigram_list=[list(bigrams(tweet)) for tweet in cleaned_tokens]
bigrams_flat=get_all_words(bigram_list)
freq_dist_bigrams=FreqDist(bigrams_flat)
print(freq_dist_bigrams.most_common(10))

network_token_df = pd.DataFrame(freq_dist_bigrams.most_common(50), columns=['token','count'])

bigrams_d=network_token_df.set_index('token').T.to_dict('records')

network_graph = nx.Graph()

for k, v in bigrams_d[0].items():
    network_graph.add_edge(k[0], k[1], weight=(v* 10))
fig, ax = plt.subplots(figsize = (20,17))
pos = nx.spring_layout(network_graph, k=1)

nx.draw_networkx(network_graph, pos,
                 font_size =20,
                 width=3,
                 node_size=50,
                 edge_color='grey',
                 node_color='blue',
                 with_labels = True,
                 ax=ax)

text_blob = []
for tweet in data ['Tweets'].tolist():
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity==0:
        sentiment="Neutral"
    elif analysis.sentiment.polarity>0:
        sentiment="Positive"
    elif analysis.sentiment.polarity<0:
        sentiment="Negative"
    text_blob.append(sentiment)
data['Sentiment'] = text_blob


labelled_tweets=data[['Tweets','Sentiment']]
labelled_tweets.drop(labelled_tweets.loc[labelled_tweets['Sentiment']=='Neutral'].index, inplace=True)

tweets_token=labelled_tweets['Tweets'].apply(word_tokenize).tolist()
cleaned_tokens = []
for tokens in tweets_token:
    rm_noise=remove_noise(tokens, stop_words)
    lemma_tokens=lemmatize_sentence(rm_noise)
    cleaned_tokens.append(lemma_tokens)
