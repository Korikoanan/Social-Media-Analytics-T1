# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 20:43:43 2022

@author: user
"""

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    def __init__(self):
        consumer_key = "3tb2uKZTbOa78pKtN9lFWh2mt"
        consumer_secret = "1a8yR9kMAEfc8DSGHbuzXi1cxzdI8BSWXPhCOTQOirUXu5xiE6"
        access_key = "823864824727646209-wjU9Kw8kRWNhwzVK5tOUgWQWTdFcaKF"
        access_secret = "LQqYO9PofZ9uytCHbz5nkmT31pzRRwBBC2O0KNwA103fP"