import requests
from datetime import date
from bs4 import BeautifulSoup as BS
from sql import createPttTable,storePttData

def parseRowEntity(rowEntities):
    articles = list()
    for row in rowEntities:
        pushCount = row.select('div.nrec')[0].text
        pushCount = int(pushCount) if len(pushCount) else 0

        titleDiv = row.select('div.title a')
        if len(titleDiv):
            titleDiv = titleDiv[0]
        else:
            continue
        link = titleDiv['href']
        title = titleDiv.text

        thisYear = date.today().year
        pubDate = row.select('div.date')[0].text.split('/')
        pubDate = date(thisYear,int(pubDate[0]),int(pubDate[1])).strftime('%Y-%m-%d')

        author = row.select('div.author')[0].text
        articles.append(dict(pushCount=pushCount,title=title,link=link,pubDate=pubDate,author=author))
    return articles

def pttCrawler(board,pages=2):
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
        articles = parseRowEntity(rowEntities)
        storePttData(board,articles)
        curPage += 1

        prePageUrl = soup.select('div.btn-group-paging a')[1]['href']
        path = root_url + prePageUrl

root_url = 'https://www.ptt.cc'
pttCrawler('CodeJob')
