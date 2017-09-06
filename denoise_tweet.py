# -*- coding: utf-8 -*-
import pandas
import sys

def tweet_filter(tweets, mode = 0):
    # normal Tweet用フィルタ処理
    if mode == 0:
        # in_reply_to_status_idとin_reply_to_user_idの値が入っているツイートを除外
        tweets = tweets[tweets["in_reply_to_status_id"].isnull() | tweets["in_reply_to_user_id"].isnull()]
        # RTされたツイート「RT @」で始まるツイートを除外
        tweets = tweets[~tweets['text'].str.contains('RT.@*')]
        return _denoise(tweets)

    # reply Tweet用フィルタ処理
    elif mode > 0:
        # in_reply_to_status_idとin_reply_to_user_idの値が入っているツイートを除外
        tweets = tweets[tweets["in_reply_to_status_id"].notnull() | tweets["in_reply_to_user_id"].notnull()]
        # RTされたツイート「RT @」で始まるツイートを除外
        tweets = tweets[~tweets['text'].str.contains('RT.@*')]
        return _denoise(tweets)

    # RT Tweet用フィルタ処理
    elif mode < 0:
        # RTされたツイート「RT @」で始まるツイート以外を除外
        tweets = tweets[tweets['text'].str.contains('RT.@*')]
        # tweets = tweets['text'].str.replace("^(RT)", "")
        return _denoise(tweets)

def _denoise(tweets):
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
    tweets = filtered[['tweet_id','text']]

    # @hogeを削除
    tweets["text"].str.replace("@\w*:?\s", "")
    
    return tweets


if __name__ == "__main__":
    args = sys.argv

    # csv import
    print(args[1])
    tweets_csv = pandas.read_csv(args[1],encoding="utf-8")

    # tweet_filter <0:RTtweet,0:normaltweet,0<:reply
    rts = tweet_filter(tweets_csv, -1)
    tweets = tweet_filter(tweets_csv, 0)
    replies = tweet_filter(tweets_csv, 1)

    # csv export
    rts.to_csv("rts_shaped.csv", header=True)
    tweets.to_csv("tweets_shaped.csv", header=True)
    replies.to_csv("replies_shaped.csv", header=True)