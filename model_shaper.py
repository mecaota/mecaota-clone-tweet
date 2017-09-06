# -*- coding: utf-8 -*-
import pandas
import numpy as np

STR_MAX = 20

def load_csv(path="",mode = 0):
    # normal Tweet用csv読み込み処理
    if mode == 0:
        path = path + "tweets_shaped.csv"
        #path = path + "tweets_minimum.csv"

    # reply Tweet用csv読み込み処理
    elif mode > 0:
        path = path + "replies_shaped.csv"

    # RT Tweet用csv読み込み処理
    elif mode < 0:
        path = path + "rts_shaped.csv"

    print("loading csv: " + path)
    return pandas.read_csv(open(path,'rU'), encoding="utf-8")

def vectrize(tweets):
    chars = [] # 全ツイート中に登場する文字列リスト
    char_indices = {} # charの1文字1文字をキーとした辞書型オブジェクト。key:文字,value:インデックス
    indices_chars = {} # charの1文字1文字を要素として持つ辞書型オブジェクト。key:インデックス,value:文字

    # char生成処理
    for i in tweets["text"]:
        for j in str(i):
            if j not in chars:
                chars.append(j)
    chars.sort()

    # char_indicesとindices_char生成処理
    for i in chars:
        index = chars.index(i)
        char_indices[i] = index
        indices_chars[index] = i

    return chars, char_indices, indices_chars

    # 文章結合後STR_MAX語ごとに文字列分割処理
def str_split(tweets):
    alltwi = ""
    sentences = []
    next_chars = []
    for i in tweets["text"]:
        alltwi += str(i)
    
    for i in range(0, len(alltwi) - STR_MAX, 3):
        sentences.append(alltwi[i: i + STR_MAX])
        next_chars.append(alltwi[i + STR_MAX])
    return sentences, next_chars

# ラベリング
def labering(tweets):
    chars, char_indices, indices_chars = vectrize(tweets)
    sentences, next_chars = str_split(tweets)

    X = np.zeros((len(sentences), STR_MAX, len(chars)),dtype=np.bool)
    Y = np.zeros((len(sentences),len(chars)),dtype=np.bool)
    for i,j in enumerate(sentences):
        for k,l in enumerate(j):
            X[i][k][char_indices[l]] = True
        Y[i][char_indices[next_chars[i]]] = True

    return X, Y


if __name__ == "__main__":
    dir = ""
    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    rts = load_csv(dir, -1)
    tweets = load_csv(dir, 0)
    replies = load_csv(dir, 1)
    X, Y = labering(tweets)
    X3, Y3 = labering(replies)
    X2, Y2 = labering(rts)
