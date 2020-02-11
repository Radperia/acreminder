from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings
import scrape
import datetime
import time


def make_message(message, s):
    #slack.chat.post_messageを用いてメッセージを送る

    for i in s:
        message = message + "\n" + i[0] + "\n" + i[1] + "\n"
    #pos_messageでslack投稿
    #channelには投稿したいチャンネル
    #messageには投稿したいメッセージ
    #as_userはTrueにすることで、urlが展開されて投稿される
    print(message)


def info():
    #先にスクレイピングしておいたコンテスト情報を格納
    s1 = scrape.scrape_active()
    s2 = scrape.scrape_upcoming()

    #コンテスト乗法が無い場合はコンテストが存在しないメッセージを送る
    if len(s1) != 0:
        print(s1, "[開催中のコンテスト一覧]")

    else:
        print("[開催中のコンテストはありません]")

    if len(s2) != 0:
        print(s2, "[予定されているコンテスト一覧]")

    else:
        print("[予定されているコンテストはありません]")


def main():
    info()
    time.sleep(2)

if __name__ == "__main__":
    main()
