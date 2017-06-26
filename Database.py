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
