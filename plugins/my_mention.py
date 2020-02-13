# coding: utf-8

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import random

@respond_to('次回のゼミ')
def seminar(message):
    message.reply('次回のゼミはありません')


@respond_to('飯屋')
def food(message):
    shop_list = ['我羅奢', '蔭山', '表裏', '中本', 'ピコピコポン', '波風', '破壊的', 'こころ', 'マック']
    message.reply(shop_list[random.randrange(len(shop_list))])


@default_reply()
def default_func(message):
    message.reply('……。')
