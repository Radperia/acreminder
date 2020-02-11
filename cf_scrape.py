from urllib import request
from bs4 import BeautifulSoup
import re
import datetime


def scrape_upcoming():
    #一週間以内に開催されるコンテストの情報を返す関数

    re_contests = []

    url = "https://codeforces.com/contests/"
    access_url = "https://atcoder.jp"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    #contest-table-upcomingのidを持つdivタグの中に一週間以内に開催されるコンテストの情報が入ってる
    contests1 = soup.find("div", id="pageContent")

    #コンテストが無かった場合 (soupにNoneが入ってしまうため)
    if contests1 is None:
        return re_contests
    contests2 = contests1.find("tbody")
    contests3 = contests2.find_all("tr")

    #今日の日時を取得
    w = datetime.datetime.today()

    #コンテストのurlと開始の日時をre_contestsに格納
    for c in contests3:
        re_contests_sub = []
        d1 = c.find("time")

        #分まで入ってるところのみスライスして渡す
        #strtotime関数でstringからdatetimeオブジェクトに返る
        t = strtotime(d1.text[:16])

        #その週の日曜までにないコンテストは格納しない
        if(t - w).days >= 7:
            break

        #formatを統一するためtimetostr関数を使う
        re_contests_sub.append(timetostr(t) + " 開始")
        d2 = c.find("a", href=re.compile("contests"))

        #コンテストページのurlもre_contests_subに格納
        re_contests_sub.append(access_url + d2.get("href"))
        re_contests.append(re_contests_sub)

    return re_contests


def strtotime(date_sub):
    #datetimeオブジェクトにして返す
    return datetime.datetime.strptime(date_sub, '%Y-%m-%d %H:%M')

def timetostr(date_sub):
    #datetimeオブジェクトをstrオブジェクトにして返す

    W = ["月", "火", "水", "木", "金", "土", "日"]
    return ('%d-%d-%d(%s) %d:%s' % (
        date_sub.year, date_sub.month, date_sub.day, W[date_sub.weekday(
        )], date_sub.hour, str(date_sub.minute).ljust(2, "0")
    ))
