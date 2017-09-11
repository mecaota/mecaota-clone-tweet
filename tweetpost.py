#coding: UTF-8
from requests_oauthlib import OAuth1Session
import json
import sys
import random

# ローカルのjsonファイル展開、返り値は辞書型


def openJSON(file):
    with open(file, 'r') as f:
        return json.load(f)


# ツイッター認証・ツイッターAPIオブジェクト生成
def oauthTwitter(api_keys):
    twitter = OAuth1Session(api_keys["CONSUMER_KEY"], api_keys["CONSUMER_SECRET"],
                            api_keys["ACCESS_TOKEN"], api_keys["ACCESS_TOKEN_SECRET"])
    return twitter


# ローカルのjsonファイル展開、返り値は辞書型
def openJSON(file):
    with open(file, 'r') as f:
        return json.load(f)


# ツイッター認証・ツイッターAPIオブジェクト生成
def oauthTwitter(api_keys):
    twitter = OAuth1Session(api_keys["CONSUMER_KEY"], api_keys["CONSUMER_SECRET"],
                            api_keys["ACCESS_TOKEN"], api_keys["ACCESS_TOKEN_SECRET"])
    return twitter


# textのツイートを投稿
def postTweet(twitter, text):
    if len(text) >= 140:
        return "error:string size is over"
    apiurl = "https://api.twitter.com/1.1/" + "statuses/update" + ".json"
    params = {"status": text}
    req = twitter.post(apiurl, params=params)
    return json.loads(req.text)


# tweet用初期化
def initTwitter():
    settings = openJSON("_twitter_settings.json")  # setting.JSON open
    api_keys = settings["API_KEY"]  # APIkey
    twitter = oauthTwitter(api_keys)  # oauth認証にてツイッターオブジェクト生成
    return twitter


if __name__ == "__main__":
    twitter = initTwitter()
    posttext = ""
    try:
        posttext = sys.argv[1]
    except IndexError:
        posttext = "hello world" + str(random.randint(0, 65535))
    req = postTweet(twitter, posttext)
    print(req)
