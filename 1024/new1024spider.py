import requests
import os
import threading
from bs4 import BeautifulSoup

host = 'https://hh.flexui.win/'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Referer':host
}

class myThred(threading.Thread):
    def __init__(self,url,dir,filename):
        threading.Thread.__init__(self)
        self.ThreadID = filename
        self.url = url
        self.dir = dir
        self.filename = filename

    def run(self):
        download_pic(self.url,self.dir,self.filename)

def download_pic(url,dir,filename):
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        with open(str(dir) + '/' + str(filename) + '.jpg', 'wb+') as f:
            f.write(req.content)
            # print('下载完成.......' + str(filename))
    else:
        print("发生错误，跳过下载....." + str(req.status_code))

def get_page(url):
    url_list = []
    html = requests.get(url,headers=headers)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text,'lxml')
    article_url = soup.select('tbody > tr > td.tal > h3 > a')
    for url in article_url:
        url = str(host) + url.get('href')
        url_list.append(url)
    return url_list

def get_article(url):
    img_all =[]
    html = requests.get(url,headers=headers)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text,'lxml')
    title = soup.select('td > h4')[0]
    title = title.get_text()
    img_urls = soup.select('div.tpc_content.do_not_catch > input')
    for img_url in img_urls:
        img_url = img_url.get('data-src')
        img_all.append(img_url)
    img_sum = len(img_all)
    print('当前帖子：\n' + str(title) + '\n共计取到 ' + str(img_sum) + ' 张图片连接......')
    if os.path.exists(title) == False:
        os.makedirs(title)
        filename = 1
        threads = []
        for imgurl in img_all:
            # download_pic(imgurl,title,filename)
            # filename += 1
            # req = requests.get(imgurl, headers=headers)
            # if req.status_code == 200:
            #     with open(str(title) + '/' + str(filename) + '.jpg', 'wb+') as f:
            #         f.write(req.content)
            #         print('下载完成.......' + str(filename))
            #         filename += 1
            # else:
            #     print("发生错误，跳过下载....." + str(req.status_code))
            thread = myThred(imgurl,title,filename)
            thread.start()
            threads.append(thread)
            filename += 1
        for t in threads:
            t.join()
        print('下载完成......共计：' +str(filename) + ' 张图片.......')
    else:
        print("文件夹已存在，跳过下载。")
i = 1
while i <= 100:
# for i in range(1,165):
    page_url = 'https://hh.flexui.win/thread0806.php?fid=16&search=&page=' + str(i)
    try:
        pagelist = get_page(page_url)
        for url in pagelist:
            if url == 'https://hh.flexui.win/read.php?tid=5877':
                print("pass")
            elif url == 'https://hh.flexui.win/htm_data/16/1106/524942.html':
                print('pass')
            elif url == 'https://hh.flexui.win/htm_data/16/1808/344501.html':
                print('pass')
            elif url == 'https://hh.flexui.win/htm_data/16/1110/622028.html':
                print('pass')
            elif url == 'https://hh.flexui.win/htm_data/16/1706/2424348.html':
                print('pass')
            elif url == 'https://hh.flexui.win/htm_data/16/1707/2519480.html':
                print('pass')
            elif url == 'https://hh.flexui.win/htm_data/16/0805/136474.html':
                print('pass')
            elif url == 'https://hh.flexui.win/htm_data/16/1109/594741.html':
                print('pass')
            elif url == 'https://hh.flexui.win/htm_data/16/1812/3351645.html':
                print('pass')
            else:
                get_article(url)
    except:
        print('发生错误....')
    i += 1