from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from slacker import Slacker
import slackbot_settings
import scrape
import cf_scrape
import datetime
import time
import re
import os
import random

def make_message(channel, slack, s, message):
    #slack.chat.post_messageを用いてメッセージを送る

    for i in s:
        message = message + "\n" + i[0] + "\n" + i[1] + "\n"
    #pos_messageでslack投稿
    #channelには投稿したいチャンネル
    #messageには投稿したいメッセージ
    #as_userはTrueにすることで、urlが展開されて投稿される
    slack.chat.post_message(channel, message, as_user = True)

def AC_info(channel, slack):
    #先にスクレイピングしておいたコンテスト情報を格納
    #s1 = scrape.scrape_active()
    s2 = scrape.scrape_upcoming()

    #コンテスト乗法が無い場合はコンテストが存在しないメッセージを送る
    #if len(s1) != 0:
    #    make_message(channel, slack, s1, "[開催中のratedコンテスト一覧]")

    #else:
    #    slack.chat.post_message(channel, "[開催中のratedコンテストはありません]", as_user = True)

    if len(s2) != 0:
        make_message(channel, slack, s2, "[今週のAtCoder ratedコンテスト一覧]")

    else:
        slack.chat.post_message(channel, "[今週のAtCoder ratedコンテストはありません]", as_user = True)

def CF_info(channel, slack):
    #AC_info同様に先にスクレイピングしておいたコンテスト情報を格納
    s1 = cf_scrape.scrape_active()
    s2 = cf_scrape.scrape_upcoming()

    if len(s1) != 0:
        make_message(channel, slack, s1, "[現在開催中のCodeforcesコンテスト一覧]")

    else:
        slack.chat.post_message(channel, "[現在開催中のCodeforcesコンテストはありません]", as_user = True)

    if len(s2) != 0:
        make_message(channel, slack, s2, "[今週のCodeforcesコンテスト一覧]")

    else:
        slack.chat.post_message(channel, "[今週のCodeforcesコンテストはありません]", as_user = True)

def main():
    #Botを動かす前にチャンネルでのBotアプリケーションの追加を忘れずに
    channel = "競プロ"

    #API tokenはslackbot_settings.pyに保存
    slack = Slacker(slackbot_settings.API_TOKEN)

    #毎時0分であることの確認
    #if datetime.datetime.today().minute()==0:
    AC_info(channel, slack)
    CF_info(channel, slack)

    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
