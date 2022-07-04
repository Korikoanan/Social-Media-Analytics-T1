# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 20:43:43 2022

@author: user
"""

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

consumer_key = "3tb2uKZTbOa78pKtN9lFWh2mt"
consumer_secret = "1a8yR9kMAEfc8DSGHbuzXi1cxzdI8BSWXPhCOTQOirUXu5xiE6"
access_key = "823864824727646209-wjU9Kw8kRWNhwzVK5tOUgWQWTdFcaKF"
access_secret = "LQqYO9PofZ9uytCHbz5nkmT31pzRRwBBC2O0KNwA103fP"

def twitter_setup():
    #Authentication and access using keys
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return api
def clean_tweet(self, tweet):
    check_place=[str(place) for place in twitter ['Place'] if str(place) != 'nan']
    punc = '''!()-[]{}:;'"\,<>./?@#$%^&_-'''
    string_place=''.join([item for item in check_place])
    for letter in string_place:
        if letter in punc:
            _place=string_place.replace(letter,"")
            #word to replace the puncuations
def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
  
def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
  
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
  
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
  
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
  
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
  
            # return parsed tweets
            return tweets
  
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
  
def main():
    # creating object of TwitterClient Class
    api = twitter_setup()
    # calling function to get tweets
    tweets = api.get_tweets(query = 'Donald Trump', count = 200)
  
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
  
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
  
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
  
if __name__ == "__main__":
    # calling main function
    main()
