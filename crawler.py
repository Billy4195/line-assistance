import requests
from datetime import date,timedelta
from bs4 import BeautifulSoup as BS
from pttHandler import *
from threading import Timer

def parseRowEntity(rowEntities,day):
    articles = list()
    for row in rowEntities:
        pushCount = row.select('div.nrec')[0].text
        try:
            pushCount = int(pushCount)
        except:
            pushCount = 0

        titleDiv = row.select('div.title a')
        if len(titleDiv):
            titleDiv = titleDiv[0]
        else:
            continue
        link = titleDiv['href']
        title = titleDiv.text

        thisYear = date.today().year
        pubDate = row.select('div.date')[0].text.split('/')
        pubDate = date(thisYear,int(pubDate[0]),int(pubDate[1]))
        if (date.today() -timedelta(days=day)) <= pubDate:
            pubDate = pubDate.strftime('%Y-%m-%d')
        else:
            continue
        author = row.select('div.author')[0].text
        articles.append(dict(pushCount=pushCount,title=title,link=link,pubDate=pubDate,author=author))
    return articles

def pttCrawler(board,pages=2,day=2):
    curPage = 0
    path =  'https://www.ptt.cc/bbs/{0}/index.html'.format(board)
    createPttTable(board)
    while curPage < pages:
        res = requests.get(path)
        soup = BS(res.text,'html.parser')
        bbsScreen = soup.find('div',{'class':'bbs-screen'})
        rows = bbsScreen.children
        rowEntities = list()
        for row in rows:
            if row == '\n':
                continue
            if 'r-list-sep' in row['class']:
                break
            rowEntities.append(row)
        articles = parseRowEntity(rowEntities,day)
        if len(articles) == 0:
            break
        storePttData(board,articles)
        curPage += 1

        prePageUrl = soup.select('div.btn-group-paging a')[1]['href']
        path = root_url + prePageUrl

def truncateTitle(articles):
    for article in articles:
        article['title'] = article['title'].replace('[發案]','').lstrip()
        if len(article['title']) > 17:
            article['title'] = article['title'][:17] + '...'
    return articles

def getCaseJobArticles(board):
    """
    return [dict(title,link),..]
    title len < 20
    """
    deleteOutdateArticles(board,day=2)
    articles = queryArticles(board)
    articles = truncateTitle(articles)
    return articles

def triggerCrawler():
    for board in ['CodeJob','soho','NCTU_TALK']:
        pttCrawler(board)

    print("Crawler finished")
    timer = Timer(7200,triggerCrawler)
    timer.start()

root_url = 'https://www.ptt.cc'

