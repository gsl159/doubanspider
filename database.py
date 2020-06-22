import pymysql
import time

class MySql():
    def __init__(self):
        self.db = pymysql.connect(

        )
        self.cursor = self.db.cursor()

    def insert_movie_data(self, data):
        # print(data)
        sql = "insert into movie(movie_id,movie_title,type,country,duration,rating,douban_url,poster,director,cast,description) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (data['movie_id'], str(data['movie_title']), str(data['type']), str(data['country']), str(data['long']), str(data['rating']),
            str(data['douban_url']), str(data['poster']), str(data['director']), str(data['cast']), str(data['description'])))
        self.db.commit()

    def insert_coments_data(self, data):
        sql = "insert into rating(movie_id,user_id,comment,rating) values(%s,%s,%s,%s)"
        self.cursor.execute(sql, (
            data['movie_id'], data['user_id'], data['comment'], data['rating']))
        self.db.commit()

    def close_databases(self):
        self.db.close()
