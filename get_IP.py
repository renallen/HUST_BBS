# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import random
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
def get_ip(url):
    ip_list=[]
    try:
        page = requests.get(url, headers=headers).text
        soup = BeautifulSoup(page, 'lxml')
        data = soup.select('li ul')[1:]
        for i in data:
            if i.select('li')[4].text == '中国':
                ip_list.append(i.select('li')[0].text+':'+i.select('li')[1].text)
    except:
        pass
    if not ip_list == []:
        print("获取IP网站："+url)
        print(ip_list)
    else:
        print("该IP网站无法获取："+url)
    return ip_list
def get_ip2(url):
    ip_list=[]
    try:
        page = requests.get(url, headers=headers).text
        soup = BeautifulSoup(page, 'lxml')
        data = soup.select('tbody  tr')

        for i in data:
            if float(i.select('td')[4].text.split(' ')[0])<2:
                ip_list.append(i.select('td')[0].text+':'+i.select('td')[1].text)
        # print(ip_list)
    except:
        pass
    if not ip_list == []:
        print("获取IP网站："+url)
        print(ip_list)
    else:
        print("该IP网站无法获取："+url)
    return ip_list
def get_ip3():
    with open('ip_pool.txt', 'r') as f:
        a = f.read()
        ip = a.split('//')[0].split('\n')[:-1]+a.split('//')[-1].split('\n')[1:-1]
    url = 'http://www.xicidaili.com/nn/'

    for j in ip:
        try:
            proxies= {
            'http': 'http://' + j
            }
            web_data = requests.get(url, headers=headers,proxies=proxies,timeout=1)
            soup = BeautifulSoup(web_data.text, 'lxml')
            ips = soup.find_all('tr')
            ip_list = []
            for i in range(1, len(ips)):
                # for i in range(1, 30):
                ip_info = ips[i]
                tds = ip_info.find_all('td')
                ip_list.append(tds[1].text + ':' + tds[2].text)
            if not ip_list == []:
                print("获取IP网站：" + url)
                print(ip_list)
                break
            else:
                print("该IP网站无法获取：" + url)
        except:
            pass
    return ip_list

def get_ip_list():
    url=['http://www.data5u.com/','http://www.data5u.com/free/country/%E4%B8%AD%E5%9B%BD/index.html','http://www.data5u.com/free/gngn/index.shtml','http://www.data5u.com/free/gnpt/index.shtml']
    ip_list=[]
    for i in url:
        ip_list=ip_list+get_ip(i)
    for i in range(1,10):
        ip_url='http://www.kxdaili.com/ipList/{}.html#ip'.format(i)
        ip_list = ip_list+get_ip2(ip_url)
        time.sleep(random.uniform(0,1))
    # ip_list = ip_list+get_ip3('http://www.xicidaili.com/')
    # print(ip_list)
    ip_list=ip_list+get_ip3()
    return ip_list
def get_ok_ip():
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    #     'Referer': 'http://bbs.whnet.edu.cn/main.html'
    #     ##referer根据需要改
    # }
    # with open('ip_pool.txt', 'r') as f:
    #     a = f.read()
    #     ip_list = a.split('//')[-1].split('\n')[1:-1]+a.split('//')[0].split('\n')[:-1]
    # url = 'http://bbs.whnet.edu.cn/'
    # ##url根据测试网页
    # ip_list =ip_list+ get_ip_list()
    # ip = []
    # for i in ip_list:
    #     proxies = {
    #         'http': 'http://' + i
    #     }
    #     try:
    #         page = requests.get(url, headers=headers, proxies=proxies, timeout=2)
    #         # print(page.text.encode('iso-8859-1').decode('gbk'))
    #         if not page.status_code == 200:
    #             # print(page.text)
    #             pass
    #         else:
    #             ip.append(i)
    #             print('更新ip中...', i)
    #     except:
    #         pass

    ip = get_ip_list()
    with open('temp.txt','r+') as f:
        a=f.read()
        for i in ip:
            if not i in a:
                f.writelines(i+'\n')
    # print('ip更新完毕。')
    return ip

if __name__ == '__main__':
    # url = 'http://www.xicidaili.com/nn/'
    ip = get_ok_ip()

                # print('写入')
    print("ip",ip)



