from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings
import scrape
import datetime
import time

def make_message(channel, slack, s, message):
    #slack.chat.post_messageを用いてメッセージを送る

    for i in s:
        message = message + "\n" + i[0] + "\n" + i[1] + "\n"
    #pos_messageでslack投稿
    #channelには投稿したいチャンネル
    #messageには投稿したいメッセージ
    #as_userはTrueにすることで、urlが展開されて投稿される
    slack.chat.post_message(channel, message, as_user = True)

def info(channel, slack):
    #先にスクレイピングしておいたコンテスト情報を格納
    s1 = scrape.scrape_active()
    s2 = scrape.scrape_upcoming()

    #コンテスト乗法が無い場合はコンテストが存在しないメッセージを送る
    if len(s1) != 0:
        make_message(channel, slack, s1, "[開催中のコンテスト一覧]")

    else:
        slack.chat.post_message(channel, "[開催中のコンテストはありません]", as_user = True)

    if len(s2) != 0:
        make_message(channel, slack, s2, "[予定されているコンテスト一覧]")

    else:
        slack.chat.post_message(channel, "[予定されているコンテストはありません]", as_user = True)    

def main():
    #Botを動かす前にチャンネルでのBotアプリケーションの追加を忘れずに
    channel = "競プロ"

    #API tokenはslackbot_settings.pyに保存
    slack = Slacker(slackbot_settings.API_TOKEN)

    #月曜であることの確認
    if datetime.datetime.today().hour == 12:
        info(channel, slack)

    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()