#-------------------------------------------------------------------------------
# Name:        ztsk.py
# Purpose: 湖南干部教育网课之专题培训班课程自动学习
#
# Author:      weauthi
#
# Created:     2020-03-12
# Copyright:   (c) Administrator 2020
# Licence:     1.0
# -------------------------------------------------------------------------------
# -*- coding:utf-8 -*-

import requests
import time
from datetime import datetime
from hnsk import get_jytoken  #从hnsk.py导入get_jytoken函数
from hnsk import get_timenode, url  # 从hnsk.py导入get_timenode函数及url常量


def getTrainningClass(userid, pagecount):
    data = {
        'method': 'getTrainningClass',
        'page': '1',
        'PageCount': pagecount,
        'UserID': userid,
        'typeid': '2'
    }
    response = requests.post(url, data=data).json()
    trainClassList = response['TrainClassInfoList']
    return trainClassList


def add_trainClass(userid, tcid):
    data = {
        'method': 'UpdateTrainningStudentup',
        'UserID': userid,
        'tcid': tcid  #查到要选的专课ID
    }
    response = requests.post(url, data=data).json()
    return response


def get_channelList(*args):
    data = {'method': 'getChannelInfoList', 'Portal': '1', 'parentId': '361'}
    response = requests.post(url, data=data).json()
    channelList = response['ChannelInfoList']
    return channelList


def get_trainCourseList(userid, channelid, tcid, page, pagecount):
    data = {
        'method': 'GetTrainingCourseList',
        'UserID': userid,
        'trainingid': tcid,
        'Page': page,
        'PageCount': pagecount,
        'Channelid': channelid,
        'portal': '1'
    }
    response = requests.post(url, data=data).json()
    trainCourseList = response['CourseInfoList']
    return trainCourseList


def add_trainCourse(userid, coursenumber, jytoken):
    data = {
        'method': 'UpdateUserCourse',
        'UserID': userid,
        'CourseNumber': coursenumber,
        'AddAndDel': 'add',
        'jytoken': jytoken
    }
    response = requests.post(url, data=data).json()
    return response


def upload_timenode(userid, coursenumber, timenode, jytoken):
    data = {
        'method': 'UploadTimeNode',
        'UserID': userid,
        'Coursenumber': coursenumber,
        'TimeNode': timenode,
        'Portal': '1',
        'jytoken': jytoken
    }
    response = requests.post(url, data).json()
    return response


if __name__ == '__main__':
    pagecount = 10000
    page = 1
    userid = input(u'请输入用户ID：')
    tClass = getTrainningClass(userid, pagecount)
    print(
        u'--------------------------------------目前可以报名的培训班列表----------------------------\n'
    )
    print(u'培训班ID', u'                培训班名称', u'                       报名截止时间')
    print(
        '--------------------------------------------------------------------------------------'
    )
    now = datetime.now()
    for i, tc in enumerate(tClass):
        tc_Name = tc['tc_Name']
        tc_ID = tc['tc_ID']
        tc_SignEndTime = tc['tc_SignEndTime']
        if tc_SignEndTime > str(now):
            print(tc_ID, '             ', tc_Name, '      ', tc_SignEndTime)
    print(
        '---------------------------------------------------------------------------------------'
    )
    tcid = input(u'请输入培训班ID：')
    print(
        '---------------------------------------------------------------------------------------'
    )

    #courselist = [i for i in get_CourseInfoList(userid, pagecount, page) if float(i['Credit_hour']) >= 1]

    #coursecount = len(courselist)
    #selenumber = random.randrange(70, coursecount)
    print(u'\t报名返回值：', add_trainClass(userid, tcid))
    channelList = get_channelList()
    starttime = time.time()
    for i, channelid in enumerate(channelList):
        cid = str(channelid['Channel_id'])
        courselist = [
            j for j in get_trainCourseList(userid, cid, tcid, page, pagecount)
        ]
        print(cid)
        #coursecount = len(courselist)
        #print(u'-----------------添加了专题培训课程：{}个，选择{}个开始学习--------------------'.format(coursecount, coursecount))
        for i, course in enumerate(courselist):
            coursenumber = course['Course_Number']
            print(u'{}、正在学习的课程：{}'.format(i + 1, course['Course_Name']))

            # 选课
            jytoken = get_jytoken(userid, coursenumber)
            print(u'\t选课返回值：', add_trainCourse(userid, coursenumber, jytoken))

            # 完成学习
            timenode = get_timenode()
            jytoken = get_jytoken(userid, coursenumber, timenode)
            print(u'\t提交完成学习进度的返回值：',
                  upload_timenode(userid, coursenumber, timenode, jytoken))

    print(u'学习总用时：{:.2f}秒'.format((time.time() - starttime)))