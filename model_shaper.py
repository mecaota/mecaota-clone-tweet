# -*- coding: utf-8 -*-
import pandas
import re
import numpy
import sys

STR_MAX = 20

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
    char = []
    char_indices = {}
    indices_char = {}

    # char生成処理
    for i in tweets["text"]:
        for j in i:
            if j not in char:
                char.append(j)
    char.sort()

    # char_indicesとindices_char生成処理
    for i in char:
        index = char.index(i)
        char_indices[i] = index
        indices_char[index] = i

    return char, char_indices, indices_char

    # 文章結合後STR_MAX語ごとに文字列分割処理
def str_split(tweets):
    alltwi = ""
    sentence = []
    next_chars = []
    for i in tweets["text"]:
        alltwi += i
    
    for i in range(0, len(alltwi), 3):
        try:
            sentence.append(alltwi[i: i + STR_MAX])
            next_chars.append(alltwi[i + STR_MAX + 1])
        except IndexError:
            break

    return sentence, next_chars

if __name__ == "__main__":
    dir = ""
    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    #rts = load_csv(dir, -1)
    tweets = load_csv(dir, 0)
    replies = load_csv(dir, 1)
    char, char_indices, indices_char = vectrize(tweets)
    sentence, next_chars = str_split(tweets)

    # csv output
    print(char)
    print(char_indices)
    print(indices_char)
    print(sentence)