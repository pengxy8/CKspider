#!env/bin/python
# -*- coding:utf8 -*-
import re,sys
import requests
import threading

def getHref(myDir, f, url, start, step):
    # 在一页中找到内容html
    patternForHTML = re.compile('<div class="fl main">.*?<div class="ck-product-list">.*?<ul class="clearfix">(.*?)</ul>', re.S)
    # 在内容html中匹配课程url
    patternForHref = re.compile('<div class="item-panel">.*?<div class="item-pic">.*?<a href="(.*?)" target="_blank">', re.S)
    page = start
    while True:
        html = requests.get(url, params = {'page': page}).text
        # 判断是否抓取失败，若失败则重新抓取
        while html == 'Can\'t Create SessionID, Exit':
            print('bad')
            import time
            time.sleep(5)
            html = requests.get(url, params = {'page': page}).text
        htmlf = open(myDir+'/'+str(page)+'.html', 'w')
        # 将html存下
        htmlf.write(html)
        htmlf.close()
        # 找到内容html
        content = patternForHTML.search(html)
        if content:
            # 在内容html中搜索课程url
            hrefList = patternForHref.findall(content.group(1))
        else:
            # 无更多商品或页数达到50以上时将会匹配不到内容，此时退出循环
            break
        # 将结果打印到文件
        f.write('\n'.join(hrefList) + '\n')
        page += step
        

def getMsg(day, f, fin):
    # 在课程详情页中匹配价格和购买人数
    patternForMsg = re.compile('<div class="details-topcon">.*?<h3 class="title">(.*?)</h3>.*?<li class="price">.*?<span class="fl num"><em class="money">¥</em>(.*?)</span>.*?<li class="purchase">.*?<em class="c-333">(.*?)</em>', re.S)
    # 遍历url文件
    for url in fin:
        html = requests.get(url).text
        # 判断是否抓取失败，若失败则重新抓取
        while html == 'Can\'t Create SessionID, Exit':
            print('bad')
            import time
            time.sleep(5)
            html = requests.get(url).text
        # 将html存下
        htmlf = open('day%s/html/%s' % (day, url.split('/')[-1]), 'w')
        htmlf.write(html)
        htmlf.close()
        # 匹配价格和购买人数
        msg = patternForMsg.search(html)
        if msg:
            # 写入文件
            f.write(url + ' ' + ' '.join(msg.groups()) + '\n')
        else:
            error = open('day%s/error.txt' % day, 'a')
            error.write(url)
            print(html)
            print(patternForMsg)
            # 如果匹配不到将url打印出来，手动检查并找出原因
            print(url)


def spiderForUrl(myDir, day, url):
    print('start to get the urls')

    # 单线程
    hreflist = open('day%s/hreflist.txt' % day, 'a')
    getHref(myDir, hreflist, url, 1, 1)
    hreflist.close()

    # 双线程抓取url，分别抓单双页数的url，然后存在两个文件中
    # hreflist1 = open('day%s/hreflist1.txt' % day, 'a')
    # hreflist2 = open('day%s/hreflist2.txt' % day, 'a')
    # hrefT1 = threading.Thread(target=getHref, args=(hreflist1, url, 1, 2), name='t1')
    # hrefT1.start()
    # hrefT2 = threading.Thread(target=getHref, args=(hreflist2, url, 2, 2), name='t2')
    # hrefT2.start()
    # hrefT1.join()
    # hrefT2.join()
    # hreflist1.close()
    # hreflist2.close()

    print('done')


def spiderForMsg(day):
    print('start to get the msg')

    # 单线程
    msg = open('day%s/msg.txt' % day, 'a')
    hreflist = open('day%s/hreflist.txt' % day, 'r')
    getMsg(day, msg, hreflist)
    msg.close()
    hreflist.close()

    # 双线程抓取价格及购买人数，分别从两个文件中读取url
    # msg1 = open('day%s/msg1.txt' % day, 'a')
    # msg2 = open('day%s/msg2.txt' % day, 'a')
    # hreflist1 = open('day%s/hreflist1.txt' % day, 'r')
    # hreflist2 = open('day%s/hreflist2.txt' % day, 'r')
    # msgT1 = threading.Thread(target=getMsg, args=(msg1, hreflist1), name='t1')
    # msgT1.start()
    # msgT2 = threading.Thread(target=getMsg, args=(msg2, hreflist2), name='t2')
    # msgT2.start()
    # msgT1.join()
    # msgT2.join()
    # msg1.close()
    # msg2.close()
    # hreflist1.close()
    # hreflist2.close()

    print('done')
