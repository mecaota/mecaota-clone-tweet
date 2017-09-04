# -*- coding: utf-8 -*-
import pandas
import numpy
import sys

args = sys.argv

# csv import
tweets = pandas.read_csv(args[1],encoding="utf-8")

# in_reply_to_status_idとin_reply_to_user_idの値が入っているツイートを除外
tweets = tweets[tweets["in_reply_to_status_id"].isnull() | tweets["in_reply_to_user_id"].isnull()]

print(tweets)

# csv export
tweets.to_csv("tweets_shaped.csv")