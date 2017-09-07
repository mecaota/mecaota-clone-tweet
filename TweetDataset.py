# -*- coding: utf-8 -*-
import pandas
import numpy as np

### TweetDataset ###
class TweetDataset:
    def __init__(self, path):
        self.tweets = pandas.read_csv(open(path,'rU'), encoding="utf-8")
        print("TweetModel instance create task start from " + str(path))
        self.strmax = 20
        self.sentences = []
        self.next_chars = []
        self.chars = []
        self.char_indices = {}
        self.indices_chars = {}
        self.alltweet = ""
        self.__str_split()
        self.__vectrize()

        self.X = np.zeros((len(self.sentences), self.strmax, len(self.chars)),dtype=np.bool)
        self.Y = np.zeros((len(self.sentences),len(self.chars)),dtype=np.bool)
        print("TweetModel labeling start " + str(path))
        self.__labering()
    
    # このオブジェクト内の再利用データをdict型で返す
    def to_dict(self):
        dataset = {}
        dataset["strmax"] = self.strmax
        dataset["sentence"] = self.sentences
        dataset["next_chars"] = self.next_chars
        dataset["chars"] = self.chars
        dataset["char_indices"] = self.char_indices
        dataset["indices_chars"] = self.indices_chars
        dataset["alltweet"] = self.alltweet
        dataset["X"] = self.X
        dataset["Y"] = self.Y
        return dataset

    # 文章結合後STR_MAX語ごとに文字列分割処理
    def __str_split(self):
        alltwi = ""
        sentences = []
        next_chars = []
        for i in self.tweets["text"]:
            alltwi += str(i)
        self.alltweet = alltwi
        
        for i in range(0, len(alltwi) - self.strmax, 3):
            sentences.append(alltwi[i: i + self.strmax])
            next_chars.append(alltwi[i + self.strmax])

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
    tweets = TweetDataset("mini_tweets_shaped.csv")
    replies = TweetDataset("mini_replies_shaped.csv")
    rts = TweetDataset("mini_rts_shaped.csv")
