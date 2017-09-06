# -*- coding: utf-8 -*-
import pandas
import numpy as np

STR_MAX = 20

class TweetModel:
    def __init__(self, path):
        self.tweets = pandas.read_csv(open(path,'rU'), encoding="utf-8")
        self.strmax = 20
        self.sentences = []
        self.next_chars = []
        self.chars = []
        self.char_indices = {}
        self.indices_chars = {}
        self.__str_split()
        self.__vectrize()
        print("TweetModel instance created from " + str(path))

        self.X = np.zeros((len(self.sentences), STR_MAX, len(self.chars)),dtype=np.bool)
        self.Y = np.zeros((len(self.sentences),len(self.chars)),dtype=np.bool)
        self.__labering()
        
    # 文章結合後STR_MAX語ごとに文字列分割処理
    def __str_split(self):
        alltwi = ""
        for i in self.tweets["text"]:
            alltwi += str(i)
        
        for i in range(0, len(alltwi) - STR_MAX, 3):
            self.sentences.append(alltwi[i: i + STR_MAX])
            self.next_chars.append(alltwi[i + STR_MAX])

    def __vectrize(self):
        # char生成処理
        for i in self.tweets["text"]:
            for j in str(i):
                if j not in self.chars:
                    self.chars.append(str(j))
        self.chars.sort()

        # char_indicesとindices_char生成処理
        for index, i in enumerate(self.chars):
            self.char_indices[i] = index
            self.indices_chars[index] = str(i)

    # ラベリング
    def __labering(self):
        for i,j in enumerate(self.sentences):
            for k,l in enumerate(j):
                self.X[i][k][self.char_indices[l]] = True
            self.Y[i][self.char_indices[self.next_chars[i]]] = True

if __name__ == "__main__":
    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    rts = TweetModel("rts_shaped.csv")
    #tweets = TweetModel("tweets_minimum.csv")
    tweets = TweetModel("tweets_shaped.csv")
    replies = TweetModel("replies_shaped.csv")
