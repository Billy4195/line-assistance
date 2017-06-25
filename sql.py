import psycopg2

class Database():
    def __init__(self):
        try:
            conn = psycopg2.connect(database='billy',user='billy',password='gbhty123',host='127.0.0.1')
            cur = conn.cursor()
            self.conn = conn
            self.cur = cur
        except Exception as e:
            print(str(e))

    def cmd(self,sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(str(e))

    def query(self,sql):
        try:
            return self.cur.execute(sql)
        except Exception as e:
            print(str(e))

def createPttTable(board):
    db = Database()

    sql = 'CREATE TABLE IF NOT EXISTS {0} (' \
                'title varchar[512],' \
                'link varchar[256],' \
                'pushCount int,' \
                'pubDate date,' \
                'author varchar[256],' \
                'visited int default 0);'.format(board)
    db.cmd(sql)
    db.close()

createPttTable('CodeJob')

