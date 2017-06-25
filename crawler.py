import requests
from bs4 import BeautifulSoup as BS

def parseRowEntity(rowEntities):
    articles = list()
    for row in rowEntities:
        pushCount = row.select('div.nrec')[0].text
        pushCount = int(pushCount) if len(pushCount) else 0

        titleDiv = row.select('div.title a')[0]
        link = titleDiv['href']
        title = titleDiv.text

        date = row.select('div.date')[0].text
        author = row.select('div.author')[0].text
        articles.append(dict(pushCount=pushCount,title=title,link=link,date=date,author=author))
        print(dict(pushCount=pushCount,title=title,link=link,date=date,author=author))

def pttCrawler(board,pages=2):
    curPage = 0
    path =  'https://www.ptt.cc/bbs/{0}/index.html'.format(board)

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
        parseRowEntity(rowEntities)
        curPage += 1

        prePageUrl = soup.select('div.btn-group-paging a')[1]['href']
        path = root_url + prePageUrl

root_url = 'https://www.ptt.cc'
pttCrawler('CodeJob')
