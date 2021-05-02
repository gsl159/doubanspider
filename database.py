import pymysql
import time
import random


class MySql():
    def __init__(self):
        self.db = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='456456asd',
            database='yangtuo',
            port=3306,
            charset='utf8mb4'
        )
        self.cursor = self.db.cursor()

    def getMovieIds(self):
        sql = "select movie_id from movie"
        result = self.cursor.execute(sql)
        return self.cursor.fetchall()

    def transMid2MovieId(self, mid):
        sql = "SELECT movie_id from movie where mid = " + str(mid)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def updatePoster(self, data):
        sql = "update movie set poster = %s,douban_url = %s where movie_id = %s"
        self.cursor.execute(sql, [data['poster'], data['douban_url'], data['movie_id']])

    def insert_movie_data(self, data):
        # print(data)
        sql = "insert into movie(movie_id,movie_title,type,country,duration,rating,douban_url,poster,director,cast,description) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (
            data['movie_id'], str(data['movie_title']), str(data['type']), str(data['country']), str(data['long']),
            str(data['rating']),
            str(data['douban_url']), str(data['poster']), str(data['director']), str(data['cast']),
            str(data['description'])))
        self.db.commit()

    def insert_coments_data(self, data):
        sql = "insert into rating(movie_id,user_id,comment,rating,rate_time) values(%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (
            data['movie_id'], data['user_id'], data['comment'], data['rating'], self.mkdate()))
        self.db.commit()

    def close_databases(self):
        self.db.close()

    def get_done(self):
        sql = "select movie_id from rating"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        list = []
        for item in result:
            list.append(item[0])
        return list

    def insertUser(self):
        sql = "insert into user(user_id,username,password,nickname) values(%s,%s,%s,%s)"
        charSet = ['杨', '中', '羊', '驼', '阳', '只', 'Neo', '熏', '爱', '我', '可', '哈', 'a', 'b', 'c', 'd', 'e', 'f', '1', 'g',
                   'h', '35', '24123', 'h', 'm', 'c', 'd', '鹅', '丽萨', '(⊙﹏⊙)', '高', '的', '吖', '方', '史蒂夫', '是', 'の']
        nameSet = ['a', 'b', 'c', 'd', 'e', 'f', '1', 'g', 'h', '35', '24123']
        for i in range(1, 300):
            nickname = ''.join(random.sample(charSet, 3))
            username = ''.join(random.sample(nameSet, 6))
            password = '123'
            self.cursor.execute(sql, (str(i), username, password, nickname))
            self.db.commit()

    def mkdate(self):
        a1 = (2016, 1, 1, 0, 0, 0, 0, 0, 0)  # 设置开始日期时间元组（1976-01-01 00：00：00）
        a2 = (2020, 6, 31, 23, 59, 59, 0, 0, 0)  # 设置结束日期时间元组（1990-12-31 23：59：59）
        start = time.mktime(a1)  # 生成开始时间戳
        end = time.mktime(a2)  # 生成结束时间戳
        t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
        date_touple = time.localtime(t)  # 将时间戳生成时间元组
        date = time.strftime("%Y-%m-%d", date_touple)  # 将时间元组转成格式化字符串（1976-05-21）
        return date

    def recommend(self):
        sql = "select movie_id from movie"
        self.cursor.execute(sql)
        movieIds = self.cursor.fetchall()
        for movie in movieIds:
            sql_1 = "SELECT movie_id as rec_id FROM recommend where recommend.user_id in (select user_id from recommend where movie_id = " + str(
                movie[0]) + ") GROUP BY movie_id ORDER BY count(movie_id) DESC LIMIT 12"
            self.cursor.execute(sql_1)
            recs = self.cursor.fetchall()
            if len(recs) == 0:
                continue
            for recItem in recs:
                sql_2 = "insert into rec(movie_id,movie_id_recommend) values(%s,%s)"
                self.cursor.execute(sql_2, (str(movie[0]), str(recItem[0])))
                self.db.commit()
            print("-------")

    def insertRatingCSV(self, data):
        sql = "insert into rating(cid,movie_id,user_id,comment,rating,rate_time) values(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (data['cid'],
                                  data['movie_id'],
                                  data['user_id'],
                                  str(data['comment']),
                                  data['rating'],
                                  data['rate_time']))
        self.db.commit()

    def insertUserCSV(self, data):
        sql = "insert into user(user_id,username,password,nickname) values(%s,%s,%s,%s)"
        self.cursor.execute(sql, (data['user_id'],
                                  data['username'],
                                  data['password'],
                                  str(data['nickname'])))
        self.db.commit()

    def moveToDB(self, data):
        # print(data)
        sql = "insert into movie(mid,movie_id,movie_title,title_other,genre,country,duration,rating,douban_url,poster,director,cast,description,language,release_date,tag) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (data['mid'],
                                  data['movie_id'],
                                  str(data['movie_title']),
                                  str(data['title_other']),
                                  str(data['genre']),
                                  str(data['country']),
                                  str(data['duration']),
                                  str(data['rating']),
                                  str(data['douban_url']),
                                  str(data['poster']),
                                  str(data['director']),
                                  str(data['cast']),
                                  str(data['description']),
                                  str(data['language']),
                                  str(data['release_date']),
                                  str(data['tag'])))
        self.db.commit()

