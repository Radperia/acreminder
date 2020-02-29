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

def AC_make_message(channel, slack, s, message):
    for i in s:
        message = message + "\n" + i[0] + "\n" + i[1]

    slack.chat.post_message(channel, message, as_user = True)

def CF_make_message(channel, slack, s, message):
    for j in range(sum(len(v) for v in s)):
        message = message + "\n" + s[0][j]

    slack.chat.post_message(channel, message, as_user = True)

def AC_info(channel, slack):

    s1 = scrape.scrape_upcoming()

    if len(s1) != 0:
        AC_make_message(channel, slack, s1, "[今週のAtCoder ratedコンテスト一覧]")

    else:
        slack.chat.post_message(channel, "[今週のAtCoder ratedコンテストはありません]", as_user = True)

def CF_info(channel, slack):

    s1 = cf_scrape.scrape_active()
    s2 = cf_scrape.scrape_upcoming()

    if len(s1) != 0:
        CF_make_message(channel, slack, s1, "[現在開催中のCodeforcesコンテスト一覧]")

    else:
        slack.chat.post_message(channel, "[現在開催中のCodeforcesコンテストはありません]", as_user = True)

    if len(s2) != 0:
        CF_make_message(channel, slack, s2, "[今週のCodeforcesコンテスト一覧]")

    else:
        slack.chat.post_message(channel, "[今週のCodeforcesコンテストはありません]", as_user = True)

def main():

    channel = "競プロ"

    slack = Slacker(slackbot_settings.API_TOKEN)

    if datetime.datetime.today().hour() == 0:
        AC_info(channel, slack)
        CF_info(channel, slack)

    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
