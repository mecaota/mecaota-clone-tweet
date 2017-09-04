# -*- coding: utf-8 -*-
import pandas
import numpy
import sys

args = sys.argv
tweets = pandas.read_csv(args[1],encoding="utf-8")
print(len(tweets))


tweets = tweets[tweets["in_reply_to_status_id"].isnull() | tweets["in_reply_to_user_id"].isnull()]
print(tweets)

tweets.to_csv("tweets_shaped.csv")