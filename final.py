#!env/bin/python
# -*- coding:utf-8 -*-
import sys,os
# 数据结构：
# data = {'id': {'name': name, 'total': total, 'num': num}}
# data是一个字典，它的一个键值对代表一个课程，每个键值对的值也是一个字典，存有name, total, num三个键，分别代表名字，总额，购买人数

def readMsg(data, day):
    f = open('day%s/msg.txt' % day, 'r')
    while True:
        # 读取文件，一条数据占两行
        line1 = f.readline()
        if not line1:
            break
        line2 = f.readline()
        # 从url中取id
        id = line1.split('/')[-1].split('.')[0]
        (name,price,num) = line2.strip().rsplit(' ', 2)
        data[id] = {
                'name': name,
                'total': float(price) * int(num),
                'num': int(num)}

def main(day1, day2):
    data1 = {}
    data2 = {}
    readMsg(data1, day1)
    readMsg(data2, day2)

    # now用于存课程信息，new存新上架课程，off存下架课程
    now = open('result/now.txt', 'w')
    off = open('result/off.txt', 'w')
    new = open('result/new.txt', 'w')

    for id in data1:
        d1 = data1[id]
        if id in data2:
            # 如果data1的数据在data2中也有，那么将它存入now
            d2 = data2[id]
            now.write('%s\t%s\t%f\t%d\n' % (
                    id, d1['name'],
                    d2['total'] - d1['total'],
                    d2['num'] - d1['num']))
            # 把data2中这条数据删除
            data2.pop(id)
        else:
            # 如果data2中无这条数据，则存入off
            off.write('%s\t%s\t%f\t%d\n' % (
                    id, d1['name'],
                    d1['total'],
                    d1['num']))

    # data2中数据如今只剩下在data1中没有的，即新上架的，写入new中
    for id in data2:
        d = data2[id]
        new.write('%s\t%s\t%f\t%d\n' % (
                    id, d['name'],
                    d['total'],
                    d['num']))

    now.close()
    off.close()
    new.close()

if __name__ == '__main__':
    # if os.path.isdir('./result' % day):
    #     import shutil
    #     shutil.rmtree('./result' % day)
    os.mkdir('result')
    day1 = sys.argv[1]
    day2 = sys.argv[2]
    main(day1, day2)
