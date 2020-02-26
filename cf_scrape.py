from urllib import request
from bs4 import BeautifulSoup
import re
import datetime
import sys
import copy

def scrape_active():
    #現在開催中のコンテスト情報を返す関数

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

        if(i%6==0):
            contest_title = str(contests2[i].text)

            contest_title = contest_title.replace('\r', '')
            contest_title = contest_title.replace('\n', '')
            if("Enter »" in contest_title):
                contest_title = contest_title.replace("Enter »", '')
            contest_title = contest_title.rstrip()

            active_contests_sub.append(contest_title)

        if(i%6==2):
            start_time = strtotime(contests2[i].span.text)
            start_time += datetime.timedelta(hours=6)

            # 現在時刻より開始時刻が後の時return
            if(w - start_time).days <= 0:
                # 苦し紛れ
                del re_contests[-1][-1]
                return re_contests

            active_contests_sub.append(timetostr(start_time) + " 開始")

        if(i%6==3):
            length = contests2[i].text

            length = length.replace('\r', '')
            length = length.replace('\n', '')
            length = length.strip()

            active_contests_sub.append("コンテスト時間 " + length)

        if(i%6==5):
            try:
                contest_url = contests2[i].a.get("href")
                active_contests_sub.append(access_url + contest_url)
            except AttributeError:
                pass

        if(i%6==5):
            re_contests.append(active_contests_sub)

def scrape_upcoming():
    #1週間以内に開催されるコンテスト情報を返す関数

    re_contests = []
    upcoming_contests_sub = []

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
            contest_title = str(contests2[i].text)
            
            contest_title = contest_title.replace('\r', '')
            contest_title = contest_title.replace('\n', '')
            if("Enter »" in contest_title):
                contest_title = contest_title.replace("Enter »", '')
            contest_title = contest_title.rstrip()

            upcoming_contests_sub.append(contest_title)

        if(i%6==2):
            start_time = strtotime(contests2[i].span.text)
            start_time += datetime.timedelta(hours=6)

            if(start_time - w).days < 0:
                before_flag = True
                upcoming_contests_sub.clear()

            elif(start_time - w).days >= 7:
                print("**********************")
                print(re_contests)
                print("**********************")
                # 苦し紛れ
                #del re_contests[-1][-1]
                #del re_contests[-1]
                return re_contests

            else:
                before_flag = False
                upcoming_contests_sub.append(timetostr(start_time) + " 開始")

        if(i%6==3):
            if(before_flag is False):
                length = contests2[i].text

                length = length.replace('\r', '')
                length = length.replace('\n', '')
                length = length.strip()

                upcoming_contests_sub.append("コンテスト時間 " + length)

        if(i%6==5):
            if(before_flag is False):
                try:
                    contest_url = contests2[i].a.get("href")
                    upcoming_contests_sub.append(access_url + contest_url)

                except AttributeError:
                    return re_contests

                else:
                    re_contests.append(upcoming_contests_sub)

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
