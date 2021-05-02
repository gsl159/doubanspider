import csv
import re
import requests as req
from urllib import request
from database import MySql
import time
import random
import datetime
import proixy

agentlist = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36 Edg/89.0.774.75",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"]

proxylist = [{"http": "165.225.77.47:8800"},
             {"http": "46.4.147.246:1080"},
             {"http": "45.153.33.166:3128"},
             {"http": "05.252.161.48:8080"},
             {"http": "103.7.10.118:80"},
             {"http": "88.198.50.103:8080"},
             {"http": "05.252.161.48:8080"},
             {"http": "3.225.148.200:80"},
             {"http": "18.210.77.4:80"},
             {"http": "39.106.223.134:80"},
             {"http": "14.225.11.126:8080"},
             {"http": "183.213.26.12:3128"},
             {"http": "112.80.248.75:80"},
             {"http": "59.56.74.51:9999"},
             {"http": "116.117.134.134:81"},
             {"http": "60.255.151.82:80"},
             {"http": "220.181.111.37:80"}]

API_imdbID2doubanID = 'https://movie.douban.com/j/subject_suggest?q=tt'
API_getMovieInfo = 'http://localhost:5000/api/douban/movie?id='

movie = {
    'mid': 0,
    'movie_id': 0,
    'movie_title': '',
    'title_other': '',
    'director': '',
    'cast': '',
    'country': '',
    'genre': '',
    'language': '',
    'duration': 0,
    'description': '',
    'release_date': '',
    'tag': '',
    'poster': '',
    'rating': 0,
    'douban_url': ''
}

rating = {
    'cid': 0,
    'movie_id': 1,
    'user_id': 0,
    'comment': '111',
    'rating': 3,
    'rate_time': 0
}

db = MySql()

proxy = {}


def importRating():
    with open('ratings.csv', 'r') as f:
        reader = csv.reader(f)
        ratingList = list(reader)

        for i in range(1, len(ratingList)):
            rating['cid'] = i
            mid = ratingList[i][1]
            m = db.transMid2MovieId(mid)
            if m == None:
                continue
            rating['movie_id'] = m[0]
            rating['user_id'] = ratingList[i][0]
            rating['comment'] = '我给这部电影的打分是：' + ratingList[i][2]
            rating['rating'] = ratingList[i][2]
            rating['rate_time'] = ratingList[i][3]
            print(rating)
            db.insertRatingCSV(rating)


def importUser():
    for i in range(1, 611):
        user = {
            'user_id': i,
            'username': "user" + str(i),
            'password': '123',
            'nickname': "用户 " + str(i)
        }
        db.insertUserCSV(user)


def processList(list):
    if len(list) == 1:
        return list[0]
    else:
        str = ''
        for i in range(0, len(list)):
            str += list[i]
            if i != len(list) - 1:
                str += '/'
        return str


# 加载movie.csv
def readList():
    with open('movies.csv', 'r') as f:
        reader = csv.reader(f)
        result = list(reader)
        return result


# imdbID -> doubanID
def getDoubanId(imdbId):
    global proxy
    if len(imdbId) == 5:
        imdbId = '00' + imdbId
    elif len(imdbId) == 6:
        imdbId = '0' + imdbId
    flag = 0
    while True:
        flag += 1
        agent = random.choice(agentlist)
        headers = {'User-agent': agent,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   "Connection": "keep-alive",
                   "Host": "movie.douban.com",
                   'Cookie': '',
                   'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99',
                   'sec-ch-ua-mobile': '?0',
                   'Sec-Fetch-Dest': 'document',
                   'Sec-Fetch-Mode': 'navigate',
                   'Sec-Fetch-Site': 'none',
                   'Sec-Fetch-User': '?1',
                   'Upgrade-Insecure-Requests': '1',
                   }
        print(proxy)
        res = req.get(url=API_imdbID2doubanID + imdbId, headers=headers, proxies=proxy, allow_redirects=False)
        print(API_imdbID2doubanID + imdbId)
        print(res)
        # print(res.content)
        if res.status_code != 200:
            if flag != 1:
                sleepTime = random.randint(30, 40)
                proxy = getFreshProxy()
                print("获取豆瓣ID（IMDB ID为：" + str(imdbId) + "） 的时候被防爬虫了，等待 "
                      + str(sleepTime) + " 秒，更换IP为： "
                      + str(proxy) + " 出错时间：" + str(datetime.datetime.now()))
                time.sleep(sleepTime)
            else:
                print("获取豆瓣ID（IMDB ID为：" + str(imdbId)
                      + "） 的时候出错，重试！ 出错时间："
                      + str(datetime.datetime.now()))
                time.sleep(random.randint(3, 5))
        elif len(res.json()) == 0:
            return -1
        else:
            return res.json()[0]['id']


def getMovieDetail(movieId):
    res = req.get(API_getMovieInfo + movieId)
    # print("loading detail...")
    # print(res)
    return res.json()


def getMovieEntity(movieObject):
    data = movieObject['data']
    # print(data)
    movie['movie_id'] = data['id']
    movie['movie_title'] = data['title']
    movie['title_other'] = processList(data['aka_title'])
    movie['director'] = processList(data['director'])
    movie['cast'] = data['casts']
    movie['country'] = processList(data['countries'])
    movie['genre'] = processList(data['genres'])
    movie['language'] = processList(data['languages'])
    try:
        movie['duration'] = re.findall("\d+", data['durations'][0])[0]
    except:
        movie['duration'] = -1
        print("duration error!")
    movie['description'] = data['summary']
    movie['release_date'] = processList(data['pubdates'])
    movie['tag'] = processList(data['tags'])
    movie['poster'] = data['poster']
    movie['rating'] = data['average']
    movie['douban_url'] = data['alt']


def getFreshProxy():
    proxyIP = req.get("https://ip.jiangxianli.com/api/proxy_ip").json()['data']
    protocol = proxyIP['protocol']
    port = proxyIP['port']
    ip_address = proxyIP['ip']
    return {protocol: ip_address + ":" + port}


def spider():
    global proxy
    proxy = getFreshProxy()
    print("系统启动成功，IP：" + str(proxy))
    list = readList()
    for i in range(1, len(list)):
        if i % 10 == 0:
            time.sleep(33)
        movie['mid'] = list[i][0]
        doubanId = getDoubanId(list[i][3])
        if doubanId == -1:
            print("==================================" + str(
                list[i][0]) + "返回为[]================================================")
            continue
        res_entity = getMovieDetail(doubanId)
        getMovieEntity(res_entity)
        db.moveToDB(movie)
        print(str(list[i][0]) + " 爬虫成功！")
        sleepTime = random.randint(13, 26)
        time.sleep(sleepTime)


spider()