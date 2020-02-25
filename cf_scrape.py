from urllib import request
from bs4 import BeautifulSoup
import re
import datetime
import sys

def scrape_active():
    #現在開催中のコンテスト情報を返す関数

    contests_list = []
    re_contests = []
    active_contests_sub = []

    url = "https://codeforces.com/contests/"
    access_url = "https://codeforces.com"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    contests1 = soup.find("div" , class_ = "datatable")
    contests2 = contests1.find_all("td")

    w = datetime.datetime.today()

    for i in range(len(contests2)):
        contest_title = ""
        start_time = datetime.datetime.today()
        length = ""
        contest_url = ""

        #print("--------------------------")
        #print("Here is " + str(i))
        #print(re_contests)

        if(i%6==0):
            contest_title = str(contests2[i].text)
            contest_title = re.sub('[\r\n]+$', '', contest_title)
            active_contests_sub.append(contest_title)

        if(i%6==2):
            start_time = strtotime(contests2[i].span.text)
            start_time += datetime.timedelta(hours=6)
            # 現在時刻より開始時刻が後の時return
            if(w - start_time).days <= 0:
                # 苦し紛れ
                del contests_list[-1][-1][-1]
                return contests_list
            active_contests_sub.append(timetostr(start_time) + " 開始")

        if(i%6==3):
            length = contests2[i].text
            active_contests_sub.append(length)

        if(i%6==5):
            try:
                contest_url = contests2[i].a.get("href")
                active_contests_sub.append(access_url + contest_url)
            except AttributeError:
                pass

        if(i%6==5):
            re_contests.append(active_contests_sub)
            contests_list.append(re_contests)

def scrape_upcoming():
    #1週間以内に開催されるコンテスト情報を返す関数

    contests_list = []
    re_contests = []
    active_contests_sub = []

    url = "https://codeforces.com/contests/"
    access_url = "https://codeforces.com"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    contests1 = soup.find("div" , class_ = "datatable")
    contests2 = contests1.find_all("td")

    w = datetime.datetime.today()

    before_flag = False

    for i in range(len(contests2)):
        contest_title = ""
        start_time = datetime.datetime.today()
        length = ""
        contest_url = ""

        if(i%6==0):
            if(before_flag is False):
                contest_title = str(contests2[i].text)
                contest_title = re.sub('[\r\n]+$', '', contest_title)
                active_contests_sub.append(contest_title)

        if(i%6==2):
            start_time = strtotime(contests2[i].span.text)
            start_time += datetime.timedelta(hours=6)
            if(start_time - w).days < 0:
                before_flag = True
                active_contests_sub.clear()

            elif(start_time - w).days > 7:
                # 苦し紛れ
                del re_contests[-1]
                return re_contests

            else:
                before_flag = False
                active_contests_sub.append(timetostr(start_time) + " 開始")

        if(i%6==3):
            if(before_flag is False):
                length = contests2[i].text
                active_contests_sub.append("コンテスト時間 " + length)

        if(i%6==5):
            if(before_flag is False):
                try:
                    contest_url = contests2[i].a.get("href")
                    active_contests_sub.append(access_url + contest_url)
                except AttributeError:
                    pass

        if(i%6==5):
            if(before_flag is False):
                re_contests.append(active_contests_sub)

    return re_contests

def strtotime(date_sub):

    return datetime.datetime.strptime(date_sub, '%b/%d/%Y %H:%M')

def timetostr(date_sub):
    #datetimeオブジェクトをstrオブジェクトにして返す

    W = ["月", "火", "水", "木", "金", "土", "日"]
    return ('%d-%d-%d(%s) %d:%s' % (
        date_sub.year, date_sub.month, date_sub.day, W[date_sub.weekday()],
        date_sub.hour, str(date_sub.minute).ljust(2, "0")
    ))
