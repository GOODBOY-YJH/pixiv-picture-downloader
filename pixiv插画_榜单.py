import requests
import re
import os
from bs4 import BeautifulSoup
import time
import random
import datetime
##登陆
import requests as rq
from pyquery import PyQuery as pq
count = 0 #下载的图片数量

##模拟登陆代码转载自知乎大佬，侵删
name = "pixiv账号"
password = "密码"


baseHeader = {
    # 'Host': 'www.pixiv.net'
    'Connection': 'keep-alive',
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'Referer': 'https://accounts.pixiv.net/login',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}


def login():
    global name, password
    url = "https://accounts.pixiv.net/api/login?lang=zh"
    session = set_PHPSESSID()
    post_key = get_post_key(session)
    data = {
        "pixiv_id": name,
        "password": password,
        "post_key": post_key,
        "source": "pc",
        "ref": "wwwtop_accounts_index",
    }
    session.post(url, data, headers=baseHeader)
    print("登陆成功")
    return session

def get_post_key(s):
    """
    反爬措施：登录需要post_key参数
    """
    url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
    data = {"lang": "zh",
            "source": "pc",
            "view_type": "page",
            "ref": "wwwtop_accounts_index"
            }
    page = s.get(url=url, data=data,headers=baseHeader).content
    doc = pq(page)
    post_key = doc('[name="post_key"]')[0].value
##    print("<post_key>    ", post_key)
    return post_key

def set_PHPSESSID():
    """
    反爬措施，访问页面获得phpsessid的cookie值
    """
    s = rq.session()
    url = "https://www.pixiv.net/"
    s.get(headers=baseHeader, url=url)
    return s

################################




session = login()


def getHTMLText(url):   #获取页面信息
   try:
        r = session.get(url, timeout = 10, headers = baseHeader)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
   except:
        return '获取页面错误'
       




def ParsePage_url(UrlList, Url):#把主页面的每一张带图片的网页链接找出来
   try:
       url_0 = Url
##       可以解析每页的500张照片
       for i in range(2,12):
           html = getHTMLText(url_0)
           Urls = re.findall(r'href=\"(/artworks/[\d]{8})\"', html)
           for url in Urls:
               url = 'https://www.pixiv.net' + url
               if url not in UrlList:
                   UrlList.append(url)
           url_0 = Url + '&p=' + str(i)
   except:
##       print('错了')
       print('')




def ParsePage(ilt, html): #把每一个网页里对应的图片链接找出来
   try:
       Urls = re.findall(r'\"original\":\"(https://i\.pximg\.net/img-original/img/.*?)\"', html)
       ilt.append(Urls[0])
   except:
       print('')







def SaveImag(ilt):
    global count
    root = "C:/Users/Good Boy/Desktop/996/"
    if not os.path.exists(root):
       os.mkdir(root)

    
    for li in ilt:
        path = root + li.split('/')[-1]
        if not os.path.exists(path):
            r = session.get(li, headers = baseHeader)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                count = count + 1
                print("成功下载：" + path + ' ' + str(count) + '张')



def main():
    try:
       Day = input("请输入下载页数(每页五百张<由于pixiv访问限制大概五秒钟下载一张>):")
       if int(Day) <= 0:
           raise Exception("")
       else:
           Day = int(Day) - 1
       Url = 'https://www.pixiv.net/ranking.php?mode=daily' #正常
       today = datetime.datetime.now()
       for i in range(2, 3 + int(Day)): #选择下载哪一页
          UrlList = []
          ParsePage_url(UrlList,Url)   #解析每一页的所有图片链接
          for url in UrlList: #把每一个链接里的图片下载出来
             infoList = []
             html = getHTMLText(url)
             ParsePage(infoList, html)
             SaveImag(infoList)
             time.sleep(5)
          offset = datetime.timedelta(days=-i)
          re_date = (today + offset).strftime('%Y-%m-%d')
          Time_s = re_date.split('-')
          Time_s = Time_s[0] + Time_s[1] + Time_s[2]
          Url = 'https://www.pixiv.net/ranking.php?mode=daily' + '&date=' + Time_s
          #换页
    except:
        session.close()
        print("退出")
                
main()
session.close()
print("退出")
end = input()
