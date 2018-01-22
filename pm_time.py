# coding:utf-8
"""
pm_time.py
时间处理相关函数
~~~~~~~~~~~~~~~~~~~
creation time : 2018 1 19
author : anning
email : anning@kingtansin.com
~~~~~~~~~~~~~~~~~~~
"""

import os
import sys
import logging
import re
from datetime import datetime
from posixpath import join

import h5py
import numpy as np
from configobj import ConfigObj


def get_ymd_and_hm(file_name):
    """
    从文件名或者目录名中获取日期和时间
    :param file_name: (str)文件名
    :return:
    """
    # 从文件名中获取
    if os.path.isfile(file_name):
        pat = r'.*(\d{8}).*(\d{4})'
        m = re.match(pat, file_name)
        ymd = m.group(1)
        hm = m.group(2)
        return ymd, hm
    # 从目录名中获取
    elif os.path.isdir(file_name):
        pat = r'.*(\d*)'
        m = re.match(pat, file_name)
        ymd = m.group()[0:8]
        hm = m.group()[8:12]
        return ymd, hm
    else:
        raise ValueError()


def is_cross_time(start_date1, end_date1, start_date2, end_date2):
    """
    判断俩个时间段是否有交叉
    :param start_date1: (datetime)第一个时间范围的开始时间
    :param end_date1: (datetime)第一个时间范围的结束时间
    :param start_date2: (datetime)第二个时间范围的开始时间
    :param end_date2: (datetime)第二个时间范围的结束时间
    :return: 布尔值
    """
    if start_date2 <= start_date1 <= end_date2:
        return True
    elif start_date2 <= end_date1 <= end_date2:
        return True
    elif start_date2 >= start_date1 and end_date2 <= end_date1:
        return True
    else:
        return False


def str2date(date):
    """
    将字符串日期转换为 datetime
    :param date: (str) YYYYMMDD 或者 YYYYMM 或者 YYYY
    :return:
    """
    y = date[0:4]
    m = date[4:6]
    d = date[6:8]
    if y:
        y = int(y)
        if m:
            m = int(m)
            if d:
                d = int(d)
                date_time = datetime(y, m, d)
                return date_time
            else:
                d = 1
                date_time = datetime(y, m, d)
                return date_time
        else:
            m = 1
            d = 1
            date_time = datetime(y, m, d)
            return date_time
    else:
        raise ValueError()


def date_str2list(date_range):
    """
    将字符串格式的时间范围转换为一个列表
    :param date_range: (str) YYYYMMDD-YYYYMMDD 或者 YYYYMM-YYYYMM 或者 YYYY-YYYY
    :return: (list)
    """
    d = date_range.split('-')
    date_range = [i for i in d]
    return date_range


def get_date_range(date_range):
    """
    将字符串格式的时间范围转换为 datetime
    :param date_range: (str) YYYYMMDD-YYYYMMDD 或者 YYYYMM-YYYYMM 或者 YYYY-YYYY
    :return: (list)存放开始日期和结束日期
    """
    start_date, end_date = date_str2list(date_range)
    start_date = str2date(start_date)
    end_date = str2date(end_date)
    return [start_date, end_date]
