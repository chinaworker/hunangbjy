#-------------------------------------------------------------------------------
# Name:        hnsk.py
# Purpose:    湖南干部网络培训年度网课自动学习
#
# Author:      syszt
#
# Created:     2020-03-18
# Copyright:   (c) Administrator 2020
# Licence:     1.0
#-------------------------------------------------------------------------------


# -*- coding:utf-8 -*- 
import requests
import time
import hashlib
import random
 
url = 'http://app.hngbjy.com/api/mobile/default.aspx'
 
 
def get_jytoken(*args):
    appid = 'jyzxapp'
    privateKey = 'jyapp@001!'
    version = '20181101'
 
    datatime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    s = privateKey + "&" + appid + "&" + datatime + "&" + version + "&" + "&".join(args)
    md = hashlib.md5()
    md.update(s.encode())
    md5str = md.hexdigest()
    s = md5str + "&" + appid + "&" + datatime + "&" + version + "&" + "&".join(args)
    jytoken = ''.join('{:2X}'.format(ord(i)) for i in s)
    return jytoken
 
 
def get_CourseInfoList(userid, pagecount, page):
    data = {
        'method': 'getCourseInfoList',
        'channelname': '全部课程',
        'UserID': userid,
        'PageCount': pagecount,
        'Page': page,
        'Keyword': '',
        'Portal': '1'
    }
    response = requests.post(url, data=data).json()
    courselist = response['CourseInfoList']
    return courselist
 
 
def add_course(userid, coursenumber, jytoken):
    data = {
        'method': 'UpdateUserCourse',
        'userid': userid,
        'coursenumber': coursenumber,
        'AddAndDel': 'add',
        'jytoken': jytoken
    }
    response = requests.post(url, data=data).json()
    return response
 
 
def upload_timenode(userid, coursenumber, timenode, jytoken):
    data = {
        'method': 'UploadTimeNode',
        'userid': userid,
        'coursenumber': coursenumber,
        'timenode': timenode,
        'jytoken': jytoken
    }
    response = requests.post(url, data).json()
    return response
 
 #格式化时间点
def get_timenode():
    timenode = random.randrange(300000, 320000, 1)
    timenode = '%06d' % timenode   #时间点左对齐满足6位
    return timenode
 
 
if __name__ == '__main__':
    userid = input('请输入用户ID：')
    pagecount = 1000
    page = 1
 
    courselist = [i for i in get_CourseInfoList(userid, pagecount, page) if float(i['Credit_hour']) >= 1]
 
    coursecount = len(courselist)
    selenumber = random.randrange(70, coursecount)
 
    print('-----------------找到学分大于1.0的课程：{}个，选择{}个开始学习-----------------'.format(coursecount, selenumber))
    print()
    starttime = time.time()
    for i, course in enumerate(courselist[:selenumber]):
        coursenumber = course['Course_Number']
        print('{}、正在学习的课程：{}'.format(i + 1, course['Course_Name']))
 
        # 选课
        jytoken = get_jytoken(userid, coursenumber)
        print('\t选课返回值：', add_course(userid, coursenumber, jytoken))
 
        # 完成学习
        timenode = get_timenode()
        jytoken = get_jytoken(userid, coursenumber, timenode)
        print('\t提交完成学习进度的返回值：', upload_timenode(userid, coursenumber, timenode, jytoken))
 
    print()
    print('学习总用时：{:.2f}秒'.format((time.time() - starttime)))
    
    
