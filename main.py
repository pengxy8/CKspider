#!env/bin/python
# -*- coding:utf-8 -*-
import os
import re,sys
import requests
from spider import spiderForMsg,spiderForUrl

# 正则表达式
# 用于找到此页面下的所有课程数量
sumPattern = re.compile(r'<div class="g-sort">.*?<em class="num">(.*?)</em>', re.S)
# 用于取出此页面下的子分类导航栏部分
navPattern = re.compile(r'<div class="g-sort">.*?<ul class="con-list">.*?</li>(.*?)</ul>', re.S)
# 用于在子分类导航栏中找到子分类的地址
urlsPattern = re.compile(r'<li><a href="(.*?)" class="link">')
# 用于在子分类导航栏中找到子分类的名称（在运行时可以看到现在运行到哪了，非必要）
namePattern = re.compile(r'<li><a href=".*?" class="link">(.*?)<em class="num">')

def main(myDir, day, url):
    html = requests.get(url).text
    # 若进入失败，睡眠五秒然后重新抓取
    while html == 'Can\'t Create SessionID, Exit':
        print('bad')
        import time
        time.sleep(5)
        html = requests.get(url).text
    # 获取该分类课程数量
    sumn = sumPattern.search(html)
    # 如果没有子分类或者该分类总数小于等于一千，说明在50页内能展示完，直接调用函数抓取url
    if not sumn: # or int(sumn.group(1)) <= 1000:
        # 获取课程url
        spiderForUrl(myDir, day, url)
    else:
        # 先获取导航栏的html代码
        nav = navPattern.search(html).group(1)
        # 获取子分类的url和类别名称
        urls = urlsPattern.findall(nav)
        name = namePattern.findall(nav)
        for childname,childurl in zip(name, urls):
            # 展示页的目录结构与分类树结构一样
            childdir = myDir+'/'+childname.replace('/',' ')
            os.mkdir(childdir)
            print(childname)
            # 递归调用
            main(childdir, day, childurl)

if __name__ == '__main__':
    # 从命令行中得到第几天及需要抓取信息的url
    day = sys.argv[1]
    url = sys.argv[2]
    # 创建用于存数据的目录
    if os.path.isdir('./day%s' % day):
        import shutil
        shutil.rmtree('./day%s' % day)
    os.mkdir('./day%s' % day)
    # 用于存放展示页的html
    os.mkdir('./day%s/所有' % day)
    # 用于存放详情页的html
    os.mkdir('./day%s/html' % day)
    print(u'所有')
    # 抓取课程的url，并存到文本
    main('./day%s/所有' % day, day, url)
    # 从上一步抓取到的课程url中获取价格和购买人数信息
    spiderForMsg(day)
