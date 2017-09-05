# -*- coding: utf-8 -*-
import pandas
import re
import numpy
import sys

#define STR_MAX = 20

def load_csv(path,mode = 0):
    # normal Tweet用csv読み込み処理
    if mode == 0:
        path = path + "tweets_shaped.csv"

    # reply Tweet用csv読み込み処理
    elif mode > 0:
        path = path + "replies_shaped.csv"

    # RT Tweet用csv読み込み処理
    elif mode < 0:
        path = path + "rts_shaped.csv"
    print(path)
    return pandas.read_csv(path,encoding="utf-8")

def vectrize(tweets):
    for i in tweets[1]:
        print(i)
    return tweets


if __name__ == "__main__":
    dir = ""

    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    #rts = load_csv(dir, -1)
    tweets = load_csv(dir, 0)
    replies = load_csv(dir, 1)
    
    vector_tweets = vectrize(tweets)

    # csv output
    print(vector_tweets)