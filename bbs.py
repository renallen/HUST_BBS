
# -*- coding: utf-8 -*-

import requests
from multiprocessing import Pool
import time
import  pymongo
from bs4 import BeautifulSoup
import random
from get_IP import get_ip_list
client = pymongo.MongoClient('localhost',27017)
board_list = client['board']
main_list = board_list["main_list"]
paper_list= board_list["board_paper"]
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Mobile Safari/537.36'


refer = 'http://bbs.whnet.edu.cn/main.html'
headers = {
    'Connection':'keep-alive',
    'Accept':':text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    "User-Agent": agent,
    "Host": "bbs.whnet.edu.cn",
    "Origin": "http://bbs.whnet.edu.cn",
    "Referer": "http://bbs.whnet.edu.cn/index.html",
}

session = requests.session()
with open('ip_pool.txt', 'r') as f:
    a = f.read()
    http_all = a.split('//')[0].split('\n')[:-1] + a.split('//')[-1].split('\n')[1:-1]


def get_borad_paper(board,main_board):
    list = []
    http=http_all
    delet_ip = []
    ip_spider = []
    # print(http_all)
    ip_ok = []
    print(board['paper_num'])
    n=10
    if paper_list.find_one({'main_board':main_board+'-'+board['board']})==None:
        print("insert")
        paper_list.insert_one({'main_board': main_board + '-' + board['board'], 'list': list})

    if len(paper_list.find_one({'main_board':main_board+'-'+board['board']})['list'])<int(board['paper_num']):
        # http = get_ip_list()[0:20]
        list=paper_list.find_one({'main_board':main_board+'-'+board['board']})['list']
        print("update")
        while len(list)< int(board['paper_num']):
            url = 'http://bbs.whnet.edu.cn/cgi-bin/bbsdoc?board=' + board['board'] + '&start=%d' % (len(list)+1)
            headers['Referer'] = refer
            page =[]

            while page==[]:
                try:
                    rand=int(random.random()*len(http))
                    proxies = {
                        "http": 'http://' + http[rand],
                        "https": "https://182.114.42.246:8118"
                    }
                    page = requests.get(url, headers=headers, proxies=proxies,timeout=1)
                    if "禁止访问" in page.text:
                        print(proxies, "爬虫")
                        if not http[rand] in ip_spider:
                            ip_spider.append(http[rand])

                        if http[rand] in ip_ok:
                            ip_ok.remove(http[rand])
                        http.remove(http[rand])
                        if len(http) >= len(ip_ok) and len(http)<n:
                            break
                    else:
                        soup = BeautifulSoup(page.text, 'lxml')

                        if soup.select('center tr')[1:]==[]:
                            print(proxies, "打开错误",page.status_code)
                            if not http[rand] in ip_spider:
                                ip_spider.append(http[rand])
                            if http[rand] in ip_ok:
                                ip_ok.remove(http[rand])
                            http.remove(http[rand])
                            if len(http) >= len(ip_ok) and len(http)<n:
                                break
                        else:
                            for paper in soup.select('center tr')[1:]:
                                data = {
                                    'num': paper.select('td')[0].text,
                                    "id": paper.select('td')[2].text,
                                    "id_url": 'http://bbs.whnet.edu.cn/cgi-bin/' + paper.select('td a')[0].get('href'),
                                    "time": paper.select('td')[3].text,
                                    "title": paper.select('td')[4].text.replace(' ', '')[1:],
                                    'paper_url': 'http://bbs.whnet.edu.cn/cgi-bin/' + paper.select('td a')[1].get('href')
                                }
                                # print(data)
                                # if not data in list:
                                list.append(data)
                                print("总贴："+board['paper_num'], "当前："+data['num'])
                            if not http[rand] in ip_ok:
                                ip_ok.append(http[rand])
                            if http[rand] in ip_spider:
                                ip_spider.remove(http[rand])
                            paper_list.update_one({'main_board': main_board + '-' + board['board']},
                                                  {'$set': {'list': list}})
                            time.sleep(random.uniform(0, 2))
                            print("剩余ip：",len(http), "可用ip:",len(ip_ok),'失效ip：',len(delet_ip), '反爬ip：',len(ip_spider))
                            print(proxies, 'ok')
                            page=page.text
                except:
                    print(proxies,"无法连接")
                    delet_ip.append(http[rand])
                    if http[rand] in ip_ok:
                        ip_ok.remove(http[rand])
                    http.remove(http[rand])
                    if len(http) >= len(ip_ok) and len(http)<n:
                        break

            if len(http) >= len(ip_ok) and len(http)<n:
                print("更新ip库...")
                time.sleep(1)
                all_ip=get_ip_list()
                # for ip in all_ip:

                    # if ip in http or ip in delet_ip or ip in ip_spider:
                    #     pass
                    # else:
                    #     http.append(ip)
                http.extend(all_ip)
                http.extend(ip_spider)
                # with open('ip_pool.txt', 'w') as f:
                #     for i in ip_spider:
                #         f.writelines(i + '\n')
                #         http.append(i)
                #     f.writelines('//\n')
                #     for i in http:
                #         if not i in ip_spider:
                #             f.writelines(i + '\n')
                delet_ip.clear()
    else:
        pass
    print(main_board,board['board'])



def get_board_list(board):
    url = 'http://bbs.whnet.edu.cn' + board.get('href')
    name = board.text
    proxies = {
        "http": 'http://49.119.164.175:80',
        "https": "https://182.114.42.246:8118"
    }
    headers['Referer'] = refer

    page = requests.get(url,headers=headers,proxies=proxies).text
    soup = BeautifulSoup(page, 'lxml')
    print(soup)
    list=[]
    for paper in soup.select('center tr')[1:]:
        data = {
            'num': paper.select('td')[0].text,
            "board": paper.select('td')[3].text,
            "board_url": 'http://bbs.whnet.edu.cn/cgi-bin/' + paper.select('td a')[0].get('href'),
            "board_chinese": paper.select('td')[4].text.split(' ')[-1],
            "boss": None if paper.select('td')[5].text=='诚征版主中' else paper.select('td')[5].text,
            'paper_num': paper.select('td')[6].text
        }
        list.append(data)
        print(data['board'])
    main_list.insert_one({'main_board':name,'list':list})


def get_main_board():
    headers['Referer'] ='http://bbs.whnet.edu.cn/cgi-bin/bbslogin'
    page = requests.get('http://bbs.whnet.edu.cn/boalist.html',headers=headers).text.encode('iso-8859-1').decode('gbk')
    soup = BeautifulSoup(page, 'lxml')
    for board in soup.select(' td.mainbg > a'):
        get_board_list(board)
        time.sleep(random.uniform(1,3))





if __name__ == "__main__":

    url_login = 'http://bbs.whnet.edu.cn/cgi-bin/bbslogin'
    postdata = {
        'id': 'allenren',
        'login': '(unable to decode value)',
        'pw': 'allenren1995',
        'titletype': 'forum'
        }
    # proxies = {
    #     "http": 'http://122.72.32.88:80',
    #     "https": "https://182.114.42.246:8118"
    # }
        # ,proxies=proxies
    page = session.post(url_login, data=postdata, headers=headers)
    # get_main_board()
    print("登录")

    pool=Pool()
    for board in main_list.find():
        for list in board['list']:
             get_borad_paper(list,board['main_board'])
            # pool.apply_async(get_borad_paper, (list,board['main_board'], ))
            # time.sleep(10)
    pool.close() #关闭pool对象
    pool.join() #
