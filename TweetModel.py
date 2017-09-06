# -*- coding: utf-8 -*-
import pandas
import numpy as np

class TweetModel:
    def __init__(self, path):
        self.tweets = pandas.read_csv(open(path,'rU'), encoding="utf-8")
        print("TweetModel instance create task start from " + str(path))
        self.__strmax = 20
        self.sentences = []
        self.next_chars = []
        self.chars = []
        self.char_indices = {}
        self.indices_chars = {}
        self.__str_split()
        self.__vectrize()

        self.X = np.zeros((len(self.sentences), self.__strmax, len(self.chars)),dtype=np.bool)
        self.Y = np.zeros((len(self.sentences),len(self.chars)),dtype=np.bool)
        print("TweetModel labeling start " + str(path))
        self.__labering()
        
    # 文章結合後STR_MAX語ごとに文字列分割処理
    def __str_split(self):
        alltwi = ""
        sentences = []
        next_chars = []
        for i in self.tweets["text"]:
            alltwi += str(i)
        
        for i in range(0, len(alltwi) - self.__strmax, 3):
            sentences.append(alltwi[i: i + self.__strmax])
            next_chars.append(alltwi[i + self.__strmax])

        self.sentences = sentences
        self.next_chars = next_chars
        
    def __vectrize(self):
        # char生成処理self.chars = []
        chars = []
        char_indices = {}
        indices_chars = {}

        for i in self.tweets["text"]:
            for j in str(i):
                if j not in chars:
                    chars.append(str(j))
        chars.sort()

        # char_indicesとindices_char生成処理
        for index, i in enumerate(chars):
            char_indices[i] = index
            indices_chars[index] = str(i)

        self.chars = chars
        self.char_indices = char_indices
        self.indices_chars = indices_chars

    # ラベリング
    def __labering(self):
        for i,j in enumerate(self.sentences):
            for k,l in enumerate(j):
                self.X[i][k][self.char_indices[l]] = True
            self.Y[i][self.char_indices[self.next_chars[i]]] = True

if __name__ == "__main__":
    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    tweets = TweetModel("tweets_mini.csv")
    replies = TweetModel("replies_mini.csv")
    rts = TweetModel("rts_mini.csv")
    #tweets = TweetModel("tweets_shaped.csv")
    #replies = TweetModel("replies_shaped.csv")
    #rts = TweetModel("rts_shaped.csv")
