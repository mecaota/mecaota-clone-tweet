# -*- coding: utf-8 -*-
import pandas
import sys
import string

def tweet_filter(tweets, mode = 0, head_num = 3000):
    print()
    # normal Tweet用フィルタ処理
    if mode == 0:
        # in_reply_to_status_idとin_reply_to_user_idの値が入っているツイートを除外
        tweets = tweets[tweets["in_reply_to_status_id"].isnull() | tweets["in_reply_to_user_id"].isnull()]
        # RTされたツイート「RT @」で始まるツイートを除外
        print("Processing denoise to tweets_shaved.csv")
        tweets = tweets[~tweets['text'].str.contains('RT.@*')]
        tweets = _denoise(tweets)

    # reply Tweet用フィルタ処理
    elif mode > 0:
        # in_reply_to_status_idとin_reply_to_user_idの値が入っているツイートを除外
        tweets = tweets[tweets["in_reply_to_status_id"].notnull() | tweets["in_reply_to_user_id"].notnull()]
        # RTされたツイート「RT @」で始まるツイートを除外
        print("Processing denoise to replies_shaved.csv")
        tweets = tweets[~tweets['text'].str.contains('RT.@*')]
        tweets = _denoise(tweets)

    # RT Tweet用フィルタ処理
    elif mode < 0:
        print("Processing denoise to rts_shaved.csv")
        # RTされたツイート「RT @」で始まるツイート以外を除外
        tweets = tweets[tweets['text'].str.contains('RT.@*')]
        tweets = _denoise(tweets)

    mini_tweets = tweets.head(head_num)

    return tweets, mini_tweets

def _denoise(tweets):
    print()
    # ツイート元クライアントを指定
    exc = ['Foursquare','TwitCasting','Periscope','niconico','ツイ廃','Twitter.Web']
    inc = ['Android','TheWorld','Twitter','niconico','SobaCha','TweetDeck','Tweetbot','tw','ツイタマ','pictureadd','erased1023935','ATOK.Pad','SekaiCameraZoom','Hel1','Janetter','MateCha','ニコニコニュース']
    # ブラックリスト処理
    print("Except from noisy client web apps")
    for i in exc:
        tweets = tweets[~tweets['source'].str.contains(i)]

    # ホワイトリスト処理
    print("Include from main tweeting client web apps")
    for i in inc:
        tweets = pandas.concat([tweets,tweets[tweets['source'].str.contains(i)]])

    # データセットとして使うデータ列を選択
    print("select columns")
    tweets = tweets[['tweet_id','text']]

    # 全角半角正規化
    print("CJK hankaku to zenkaku AND zenkaku symbol to hankaku symbol")
    #for i, j in enumerate(tweets["text"]):
    #    tweets["text"][i] = format_text(j)
    tweets["text"] = tweets["text"].str.normalize("NFKC")
    
    # #_キョクナビタグのツイートを削除
    print("Exclude kyokunavi tweet")
    tweets = tweets[~tweets["text"].str.contains("#_キョクナビ")]

    # @リプとハッシュタグを空白1文字へ置換
    print("Exclude hashtag and replyuserid")
    tweets["text"] = tweets["text"].str.replace("[#]\S*\s?", " ")
    tweets["text"] = tweets["text"].str.replace("(RT\s)*@\w*(:\s)?", " ")
    
    # urlを空白1文字へ置換
    print("Exclude url")
    tweets["text"] = tweets["text"].str.replace("(http)s?://\S+\s*", " ")

    # 記号を空白1文字へ置換
    print("Convert to symbol to blank char")
    tweets["text"] = tweets["text"].str.replace("[!-/:-@[-`{-~”’・…；：]", " ")

    # 空白行を削除して空白削除
    print("Exclude blank char")
    tweets = tweets[~tweets["text"].str.contains("^\s+$")]
    tweets["text"] = tweets["text"].str.replace("\s+", "")
    tweets.dropna()
    print("------------------------------")

    return tweets


def format_text(text):
    text = unicodedata.normalize("NFKC", str(text)) # 全角半角正規化
    return text


if __name__ == "__main__":
    args = sys.argv

    # csv import
    print(args[1])
    tweets_csv = pandas.read_csv(args[1],encoding="utf-8")

    # tweet_filter <0:RTtweet,0:normaltweet,0<:reply
    rts, mini_rts = tweet_filter(tweets_csv, -1)
    tweets, mini_tweets = tweet_filter(tweets_csv, 0, 60000)
    replies, mini_replies = tweet_filter(tweets_csv, 1)

    # csv export
    rts.to_csv("tweetdata/rts_shaped.csv", header=True)
    mini_rts.to_csv("tweetdata/mini_rts_shaped.csv", header=True)
    tweets.to_csv("tweetdata/tweets_shaped.csv", header=True)
    mini_tweets.to_csv("tweetdata/mini_tweets_shaped.csv", header=True)
    replies.to_csv("tweetdata/replies_shaped.csv", header=True)
    mini_replies.to_csv("tweetdata/mini_replies_shaped.csv", header=True)

    print("Process done💃")