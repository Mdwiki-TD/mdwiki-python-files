#!/usr/bin/python3
"""

@WikiProjectMed

python t.py test

python3 core8/pwb.py tw/t

"""
#
# (C) Ibrahem Qasim, 2022
#
#
# ---
# ---
# ---
import tweepy
import twet_configs

# Create variables for each key, secret, token
consumer_key = twet_configs.consumer_key
consumer_secret = twet_configs.consumer_secret
access_token = twet_configs.access_token
access_token_secret = twet_configs.access_token_secret
bearer_token = twet_configs.bearer_token
# ---
# ---
# ---
# ---
# auth = tweepy.OAuth2BearerHandler(bearer_token)
# api = tweepy.Client(auth)
# ---
api = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
# ---
# print(dir(api))
# ---
# t = api.search_recent_tweets(tweet)
t = api.get_tweet(id=1582850820202450945)
print(t.data)
