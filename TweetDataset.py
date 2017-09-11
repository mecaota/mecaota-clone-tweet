# -*- coding: utf-8 -*-
import pandas
import numpy as np
import MeCab
from pykakasi import kakasi

STR_MAX = 20

### TweetDataset ###
class TweetDataset:
    def __init__(self, path, systemcall=[]):
        tweets = pandas.read_csv(open(path,'rU'), encoding="utf-8")
        print("TweetModel instance create task start from " + str(path))
        self.sentences = []
        self.alltweet = ""
        self.next_chars = []
        self.chars = []
        self.char_indices = {}
        self.indices_chars = {}
        self.__str_split(tweets, systemcall)
        self.__vectrize()

        self.X = np.zeros((len(self.sentences), STR_MAX, len(self.chars)),dtype=np.bool)
        self.Y = np.zeros((len(self.sentences),len(self.chars)),dtype=np.bool)
        print("TweetModel labeling start " + str(path))
        self.__labering()
    
    # このオブジェクト内の再利用データをdict型で返す
    def to_dict(self):
        dataset = {}
        dataset["sentence"] = self.sentences
        dataset["alltweet"] = self.alltweet
        dataset["next_chars"] = self.next_chars
        dataset["chars"] = self.chars
        dataset["char_indices"] = self.char_indices
        dataset["indices_chars"] = self.indices_chars
        dataset["X"] = self.X
        dataset["Y"] = self.Y
        return dataset

    # 文章結合後STR_MAX語ごとに文字列分割処理
    def __str_split(self, tweets, systemcall):
        alltwi = ""
        sentences = []
        next_chars = []
        for i in tweets["text"]:
            alltwi += str(i)

        if "-kana" in systemcall:
            print("kanjikana converting")
            alltwi = self.__kanjiconvert(alltwi)
        else:
            print("kanjikana convert skip")
        
        for i in range(0, len(alltwi) - STR_MAX, 3):
            sentences.append(alltwi[i: i + STR_MAX])
            next_chars.append(alltwi[i + STR_MAX])

        self.sentences = sentences
        self.next_chars = next_chars
        self.alltweet = alltwi
        
    def __vectrize(self):
        # char生成処理self.chars = []
        chars = []
        char_indices = {}
        indices_chars = {}

        for i in self.sentences:
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

    def __kanjiconvert(self, text):
        # kakasiによるひらがな変換
        kks = kakasi()
        kks.setMode('K', 'H') # カタカナをひらがなに変換するよう設定
        kks.setMode('J', 'H') # 漢字を平仮名にするよう設定
        conv = kks.getConverter()
        return conv.do(text)

if __name__ == "__main__":
    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    tweets = TweetDataset("tweetdata/mini_tweets_shaped.csv")
    replies = TweetDataset("tweetdata/mini_replies_shaped.csv")
    rts = TweetDataset("tweetdata/mini_rts_shaped.csv")
