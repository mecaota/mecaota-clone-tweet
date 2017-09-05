# -*- coding: utf-8 -*-
import pandas
import re
import numpy
import sys

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

if __name__ == "__main__":
    args = ["",""]

    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    #rts = load_csv(args[1], -1)
    tweets = load_csv(args[1], 0)
    replies = load_csv(args[1], 1)

    

    # csv export
    print(tweets)