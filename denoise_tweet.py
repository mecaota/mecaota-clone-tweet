# -*- coding: utf-8 -*-
import pandas
import numpy
import sys


def tweet_filter(tweets, mode = 0):
    if(mode == 0):
        # in_reply_to_status_idとin_reply_to_user_idの値が入っているツイートを除外
        tweets = tweets[tweets["in_reply_to_status_id"].isnull() | tweets["in_reply_to_user_id"].isnull()]
        return _denoise(tweets)
    else:
        # in_reply_to_status_idとin_reply_to_user_idの値が入っているツイートを除外
        tweets = tweets[tweets["in_reply_to_status_id"].notnull() | tweets["in_reply_to_user_id"].notnull()]
        return _denoise(tweets)

def _denoise(tweets):
    # RTされたツイート「RT @」で始まるツイートを除外
    tweets = tweets[~tweets['text'].str.contains('RT.@*')]

    # ツイート元クライアントを指定
    exc = ['Foursquare','TwitCasting','Periscope','niconico','ツイ廃','Twitter.Web']
    inc = ['Android','TheWorld','Twitter','niconico','SobaCha','TweetDeck','Tweetbot','tw','ツイタマ','pictureadd','erased1023935','ATOK.Pad','SekaiCameraZoom','Hel1','Janetter','MateCha','ニコニコニュース']
    # ブラックリスト処理
    for i in exc:
        tweets = tweets[~tweets['source'].str.contains(i)]
    filtered = tweets[~tweets['text'].str.contains('')]

    # ホワイトリスト処理
    for i in inc:
        filtered = pandas.concat([filtered,tweets[tweets['source'].str.contains(i)]])
    # データセットとして使うデータ列を選択
    tweets = filtered[['text','timestamp']]
    
    return tweets


if __name__ == "__main__":
    args = sys.argv

    # csv import
    print(args[1])
    tweets_csv = pandas.read_csv(args[1],encoding="utf-8")

    tweets = tweet_filter(tweets_csv, 0)
    replies = tweet_filter(tweets_csv, 1)

    # csv export
    tweets.to_csv("tweets_shaped.csv")
    replies.to_csv("replies_shaped.csv")