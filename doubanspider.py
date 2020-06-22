import json
import random
from lxml import etree
from pip._vendor import requests
import time
from database import MySql


class Spider():
    def __init__(self):
        # 总页面，在这个页面获取所有的电影URL等信息
        self.base_url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&start='
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
        }
        self.mysql = MySql()  # 初始化数据库接口

    def spider(self, page_num):
        # while True:
        #     # 为了避免由于超时导致的中断爬虫，所以添加try
        #     try:
        #         result = requests.get(self.base_url + str(page_num), headers=self.headers)
        #         # 当返回的code值不等于200时，表示数据返回错误。
        #         if result.status_code != 200:
        #             print("error!!")
        #         else:
        #             break
        #     except:
        #         print("error exception!")
        result = self.spider_request(self.base_url + str(page_num))
        # 将json转换为字典
        infos = json.loads(result)
        # 开始分析第一部分电影信息
        self.getMovieInfo(infos)

    def getMovieDetail(self, data):
        movie_id = data['movie_id']
        url_detail = "https://movie.douban.com/subject/" + movie_id
        result = self.spider_request(url_detail)
        html = etree.HTML(result)
        desc = ''
        list = html.xpath('//*[@id="link-report"]//span[@property="v:summary"]/text()')
        for item in list:
            desc = desc + ''.join(item.strip())
        data['description'] = desc

    def getMovieInfo(self, info):
        # print(info)
        movie_list = info['data']
        # print(movie_list)
        for movie in movie_list:
            data = {}
            title = movie['title']
            rate = movie['rate']
            url = movie['url']
            cover = movie['cover']
            id = movie['id']
            # 将列表的内容转化为字符串
            director = " / ".join(movie['directors'])
            cast = " / ".join(movie['casts'])

            data['movie_id'] = id
            data['movie_title'] = title
            data['rating'] = rate
            data['director'] = director
            data['douban_url'] = url
            data['poster'] = cover
            data['cast'] = cast
            # 开始分析详细电影信息
            self.getMovieDetail(data)
            self.get_movie_comment(data)
            # print(data)

    def get_movie_comment(self, data):
        movie_id = data['movie_id']
        comment_url = 'https://movie.douban.com/subject/' + movie_id + '/comments?start=0&limit=20&sort=new_score&status=P'

        # 添加movie_detail信息
        coments = self.spider_request(comment_url)
        html = etree.HTML(coments).xpath('//div[@class="movie-summary"]/span')[0]
        movie_type = " ".join(html.xpath('./p[3]/text()')).strip()
        movie_country = " ".join(html.xpath('./p[4]/text()')).strip()
        movie_long = " ".join(html.xpath('./p[5]/text()')).strip()

        data['type'] = movie_type
        data['country'] = movie_country
        data['long'] = movie_long
        # print(data)
        # 写入数据库
        self.mysql.insert_movie_data(data)

        uid_list = random.sample(range(1, 100), 60)
        t = 0
        while t < 60:
            # 如果为数字，则表示已经出错
            if coments.isdigit():
                break
            html = etree.HTML(coments)

            html = html.xpath('//div[@class="movie-summary"]/span')[0]
            comments = html.xpath("//div[@id='comments']/div[@class='comment-item']")
            for comment in comments:
                com = {}
                coments_info = comment.xpath('./div[@class="comment"]/p/span/text()')[0]
                rating = comment.xpath('./div[@class="comment"]/h3/span[2]/span[2]/@class')[0]
                rating_int = 0
                if rating == 'allstar50 rating':
                    rating_int = 5
                elif rating == 'allstar40 rating':
                    rating_int = 4
                elif rating == 'allstar30 rating':
                    rating_int = 3
                elif rating == 'allstar20 rating':
                    rating_int = 2
                elif rating == 'allstar10 rating':
                    rating_int = 1
                com['movie_id'] = movie_id
                com['user_id'] = uid_list[t]
                com['comment'] = coments_info
                com['rating'] = rating_int
                print(com)
                t = t + 1
                # 插入数据库
                self.mysql.insert_coments_data(com)
            # 获取下一页URL
            url = html.xpath('//div[@class="center"]/a[@class="next"]/@href')[0]
            # 构造下一跳信息
            comment_url = 'https://movie.douban.com/subject/' + movie_id + '/comments' + url
            time.sleep(5)

    # 网络请求
    def spider_request(self, url):
        while True:
            try:
                res = requests.get(url=url, headers=self.headers)
                if res.status_code != 200:
                    print("Error")
                    print(res.status_code)
                    return str(res.status_code)
                return res.text
            except:
                print("GET Error Exception")


mv = Spider()
# 1
mv.spider(0)
