from Database import Database
from datetime import date,timedelta

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
        sql = 'SELECT pushCount FROM {board} WHERE link = \'{{{link}}}\';'.format(board=board,link=entity['link'])
        result = db.query(sql)
        existed = len(result)
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
        else:
            pushCount = result[0][0]
            sql = 'SELECT COUNT(*) FROM {board} WHERE pushCount = {pushCount} and link = \'{{{link}}}\''.format(
                board=board,
                pushCount=entity['pushCount'],
                link=entity['link'])
            unchanged = db.query(sql)[0][0]
            if not unchanged:
                sql = 'UPDATE {board} SET pushCount = {pushCount} WHERE link = \'{{{link}}}\''.format(
                    board=board,
                    pushCount=entity['pushCount'],
                    link=entity['link'])
                db.cmd(sql)
    db.close()

def deleteOutdateArticles(board,day=2):
    db = Database()

    today = date.today()
    outDate = (today-timedelta(days=day)).strftime('%Y-%m-%d')
    sql = 'DELETE FROM {board} WHERE pubDate < \'{outDate}\''.format(board=board,outDate=outDate)
    db.cmd(sql)

    db.close()

def queryArticles(board,condition='visit'):
    countLimit = 4
    db = Database()

    articles = []
    if condition == 'visit':
        sql = 'SELECT title,link FROM {board} ORDER BY visited ASC,pubDate DESC LIMIT 4'.format(board=board)
    else:
        sql = 'SELECT title,link FROM {board} ORDER BY pushCount DESC,pubDate DESC LIMIT 4'.format(board=board)
    unvisitedArticles = db.query(sql)
    for article in unvisitedArticles:
        articles.append(dict(title=article[0][0],link=article[1][0]))

        sql = 'UPDATE {board} SET visited = visited + 1 WHERE link = \'{{{link}}}\''.format(board=board,link=article[1][0])
        db.cmd(sql)

    return articles
