# @Date:   19-Mar-2019
# @Email:  Tang@jeffery.top
# @Filename: time_util.py
# @Last modified time: 25-Mar-2019



# -*- coding: utf-8 -*-

import time
import re
from crawl_commons.utils.string_util import *


class TimeUtils(object):

    defualt_time_formats = ["%Y-%m-%d %H:%M:%S",
                           "%Y-%m-%d %H:%M",
                           "%Y-%m-%d",
                           "%Y/%m/%d",
                           "%Y.%m.%d",
                           "%Y年%m月%d日 %H:%M:%S",
                           "%Y年%m月%d日 %H:%M",
                           "%Y年%m月%d日%H:%M",
                           "%Y年%m月%d日%H时%M分",
                           "%Y年%m月%d日%H时%M分%S秒",
                           "%Y年%m月%d日 %H时%M分",
                            "%Y年%m月%d日 %H时%M分%S秒",
                            "%Y年%m月%d日",
                            ]

    @classmethod
    def convert2Mill4Format(cls,timeStr, format):
        try:
            timeMill = int(time.mktime(time.strptime(timeStr, format)) * 1000)
            if timeMill < 0:
                timeMill = 0
            return timeMill
        except ValueError as e:
            return None

    @classmethod
    def convert2Mill4Default(cls, timeStr, format,isAuto=False):
        result = None
        if StringUtils.isNotEmpty(format) and "pre_time" == format:
            result = TimeUtils.convert2Mill(timeStr)
        if result is not None:
            return result
        if StringUtils.isNotEmpty(format):
            if len(timeStr) < 10 and "-" in timeStr:
                timeStr = "20"+timeStr
            result = TimeUtils.convert2Mill4Format(timeStr,format)
        if result is not None:
            return result
        for timeFormat in TimeUtils.defualt_time_formats:
            result = TimeUtils.convert2Mill4Format(timeStr, timeFormat)
            if result is not None:
                return result
        if "小时" in timeStr or "天" in timeStr or "分" in timeStr:
            return TimeUtils.convert2Mill(timeStr)
        if isAuto:
            return 0
        else:
            return None


    @classmethod
    def convert2Mill(cls, timeStr):
        number = re.search(u'(\d+)',timeStr).group()
        numberInt = 0
        if number is not None and len(number)>0:
            numberInt = int(number)
        if u"小时" in timeStr:
            numberInt = numberInt*3600*1000
        elif u"分" in timeStr:
            numberInt = numberInt*60*1000
        elif u"天" in timeStr:
            numberInt = numberInt*24*3600*1000

        now = TimeUtils.getNowMill() - numberInt
        if now < 0:
            now = 0
        return now

    @classmethod
    def getNowMill(cls):
        return int(time.time()*1000)

    @classmethod
    def get_conent_time(cls, html, index):
        '''
        提取时间,并转化为时间戳
        @param html ：网页
        @param index ：是否强制使用第index个时间，-1为自动识别
        @return 时间戳
        '''
        # print(html)
        link_list = re.findall(
            r"((\d{4}|\d{2})(\-|\/|\.)\d{1,2}\3\d{1,2})(\s?\d{2}:\d{2})?|(\d{4}年\d{1,2}月\d{1,2}日)(\s?\d{2}:\d{2})?",
            html)
        timMill = None
        timelist = []
        timeAtLine = ''
        for line in link_list:
            timeAtLine = line[0]
            for ele in line:
                if timeAtLine.find(ele) == -1:
                    timeAtLine += ele
            try:
                timMill = TimeUtils.convert2Mill4Default(timeAtLine, "", True)
            except OverflowError:
                timMill = 0
            timelist.append(timMill)
        if index != -1 and len(timelist) > index:
            return timelist[index]
        else:
            while 0 in timelist:
                timelist.remove(0)
        for timMill in timelist:  # 取最新的时间
            if TimeUtils.getNowMill() - timMill > 86400000:  # 时间如果大于24小时，直接用
                return timMill
            elif time.localtime(time.time()).tm_mday - time.localtime(timMill / 1000).tm_mday > 1:  # 时间没小于24h但是隔天，直接用
                return timMill
            # elif len(timelist) >1:  # 不然可能是当前时间，用第二个时间
            #     return timelist[-2]
        if timelist != []:  # 如果所有时间都比较近，那么就用第一个时间
            timMill = timelist[0]
        if timMill is None:
            return 0
        if timMill < 0:
            timMill = 0
        return timMill

    # @classmethod
    # def get_conent_time(cls, html):
    #     '''
    #     提取时间,并转化为时间戳
    #     @param response
    #     @return 时间戳
    #     '''
    #     link_list = re.findall(
    #         r"((\d{4}|\d{2})(\-|\/|\.)\d{1,2}\3\d{1,2})(\s?\d{2}:\d{2})?|(\d{4}年\d{1,2}月\d{1,2}日)(\s?\d{2}:\d{2})?",
    #         html)
    #     timMill = None
    #     # print(link_list)
    #     if link_list != []:
    #         for t in link_list:
    #             if t[5] != '':
    #                 try:
    #                     time_get = t[0]
    #                     for ele in t:
    #                         if time_get.find(ele) == -1:
    #                             time_get += ele
    #                     # print(time_get)
    #                     timMill = TimeUtils.convert2Mill4Default(time_get, "", True)
    #                 except OverflowError:
    #                     i = 0
    #                     while i < len(link_list):
    #                         time_get = link_list[i][0]
    #                         for ele in link_list[i]:
    #                             if time_get.find(ele) == -1:
    #                                 time_get += ele
    #                         # print(time_get)
    #                         try:
    #                             timMill = TimeUtils.convert2Mill4Default(time_get, "", True)
    #                         except OverflowError:
    #                             i = i + 1
    #                             continue
    #                         break
    #             else:
    #                 i = 0
    #                 while i < len(link_list):
    #                     time_get = link_list[i][0]
    #                     for ele in link_list[i]:
    #                         if time_get.find(ele) == -1:
    #                             time_get += ele
    #                     # print(time_get)
    #                     try:
    #                         timMill = TimeUtils.convert2Mill4Default(time_get, "", True)
    #                     except OverflowError:
    #                         i = i + 1
    #                         continue
    #                     break
    #     if timMill is None:
    #         return 0
    #     if timMill < 0:
    #         timMill = 0
    #     return timMill
