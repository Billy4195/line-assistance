import psycopg2
from urllib.parse import urlparse
import os

class Database():
    def __init__(self):
        try:
            url = urlparse(os.environ["DATABASE_URL"])
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            """
            conn = psycopg2.connect(database='billy',user='billy',password='gbhty123',host='localhost')
            """
            cur = conn.cursor()
            self.conn = conn
            self.cur = cur
        except Exception as e:
            print('DB ERR init ' + str(e))

    def cmd(self,sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('DB ERR cmd ' + str(e))

    def query(self,sql):
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            print('DB ERR query ' + str(e))

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            print('DB ERR close ' + str(e))

def createPttTable(board):
    db = Database()

    sql = 'CREATE TABLE IF NOT EXISTS {0} (' \
                'title varchar[512],' \
                'link varchar[256] PRIMARY KEY,' \
                'pushCount int,' \
                'pubDate date,' \
                'author varchar[256],' \
                'visited int default 0);'.format(board)
    db.cmd(sql)
    db.close()

def storePttData(board,data):
    db = Database()

    for entity in data:
        sql = 'SELECT COUNT(*) FROM {board} WHERE link = \'{{{link}}}\';'.format(board=board,link=entity['link'])
        existed = db.query(sql)[0][0]
        if not existed:
            sql = 'INSERT INTO {board} (title,link,pushCount,pubDate,author) VALUES '\
                    '(\'{{{title}}}\',\'{{{link}}}\',{pushCount},\'{pubDate}\',\'{{{author}}}\');'.format(
                    board=board,
                    title=entity['title'],
                    link=entity['link'],
                    pushCount=entity['pushCount'],
                    pubDate=entity['pubDate'],
                    author=entity['author'])
            db.cmd(sql)
    db.close()
