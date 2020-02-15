from urllib import request
from bs4 import BeautifulSoup
import re
import datetime
import sys

def scrape_upcoming():
    #一週間以内に開催されるコンテストの情報を返す関数

    re_contests = []

    url = "https://codeforces.com/contests/"
    access_url = "https://codeforces.com"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    contests1 = soup.find("div", class_ = "datatable")
    contests2 = contests1.find_all("tr")

    w = datetime.datetime.today()

    #print(len(contests2))

    for i in range(len(contests2)):
        re_contests_sub = []

        if(i == 0):
            continue

        d1 = contests2[i].find_all("a")

        for j in range(len(d1)):
            #print("here is " + str(j))
            #print(d1[j])
            #print("---------------------------")

            if(j != 0):
                time_container = d1[j].find("span")
                if(time_container is None):
                    continue

                # tがコンテスト開催時刻を保有
                t = strtotime(time_container.text)
                t += datetime.timedelta(hours=6)

                if(t - w).days >= 7:
                    break

                re_contests_sub.append(t.strftime('%Y-%m-%d-%a %H:%M') + " 開始")
                #print(re_contests_sub)

                #d2 = d1[j].find("a", class_="contestParticipantCountLinkMargin")
                #print(type(d2))

                #print("HERE IS D1")
                #print(d1[j])
                #if(d2 is None):
                #    continue
                d2 = d1[j+1].get("href")
                #print("HERE IS D2")
                #print(d2)
                if(d2 is None):
                    continue
                re_contests_sub.append(access_url + d2)
                re_contests.append(re_contests_sub)

    return re_contests

def strtotime(date_sub):

    return datetime.datetime.strptime(date_sub, 
    '%b/%d/%Y %H:%M')
