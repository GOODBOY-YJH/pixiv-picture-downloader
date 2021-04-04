import requests
import re
import os
count = 0
select_s = ['4Kfengjing','4Kmeinv','4Kyouxi','4Kdongman','4Kyingshi','4Kmingxing','4Kqiche','4Kdongwu','4Krenwu','4Kmeishi','4Kzongjiao','4Kbeijing']
number = input("请选择分类(输入数字):\n1. 4K风景\n2. 4美女\n3. 4K游戏\n4. 4K动漫\n5. 4K影视\n6. 4K明星\n7. 4K汽车\n8. 4K动物\n9. 4K人物\n10. 4K美食\n11. 4K宗教\n12. 4K背景\n")
    
def getHTMLText(url):#获取页面信息
   try:
        kv = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }
        r = requests.get(url, timeout = 10, headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
   except:
        return '获取页面错误'
       

def ParsePage(ilt, html): #把每一个网页里对应的图片下载出来
   try:
       imag_s = re.findall(r'img src=\"/[a-z]+/[a-z]+/[0-9]+/[0-9]+-[\w]+\.jpg\" data',html)
       imags = 'https://pic.netbian.com' + imag_s[0].split('"')[1]
       ilt.append(imags)
   except:
       print('')

def ParsePage_1(ilt, html):#把主页面的每一张带图片的网页链接找出来
   try:
       imag_s = re.findall(r'a href=\"/tupian/[\d]+\.html\" target',html)
       for im in range(len(imag_s)):
          imags = 'https://pic.netbian.com' + imag_s[im].split('"')[1]
          ilt.append([imags])
   except:
       print('')

def SaveImag(ilt):
    global count
    root = "C:/Users/Good Boy/Desktop/" + select_s[int(number) - 1] + "/"
    if not os.path.exists(root):
       os.mkdir(root)
    kv = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }
    for li in ilt:
        path = root + li.split('/')[-1]
        if not os.path.exists(path):
            r = requests.get(li, headers = kv)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                count = count + 1
                print("成功下载：" + path + ' ' + str(count) + '张')

def main():
   try:
      Url = 'https://pic.netbian.com/4kdongman'
      for i in range(20): #选择下载哪一页，每页大概20张图
         imagList = []
         Html = getHTMLText(Url)    #解析每一页的所有图片链接
         ParsePage_1(imagList, Html)
         for imag in imagList: #把每一个链接里的图片下载出来
            url = imag[0]
            infoList = []
            html = getHTMLText(url)
            ParsePage(infoList, html)
            SaveImag(infoList)
            
         Url = 'https://pic.netbian.com/' + select_s[int(number) - 1] + '/index_' + str(i + 2)+ '.html'
         #换页
   except:
      print("结束")

main()
print("结束")
end = input()
