# coding:utf-8
"""
pm_calculate.py
计算相关函数
~~~~~~~~~~~~~~~~~~~
creation time : 2018 1 19
author : anning
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


def get_centre_point_avg_and_std(dataset, data_range):
    """
    计算数据集的平均值和标准差，二维或者三维
    :param dataset: (np.ndarray)获取的数据集
    :param data_range: (int)截取范围大小
    :return:(list)
    """
    # 获取数据表的维数
    rank = dataset.ndim

    if rank == 2:  # 与通道数无关
        # 获取轴数
        shape = dataset.shape
        dim = int(shape[0])
        avg_and_std = calculate_centre_point_avg_and_std(dataset, dim, data_range)
        return avg_and_std

    elif rank == 3:  # 多条通道
        # 获取轴数
        shape = dataset.shape
        channel_num = int(shape[0])  # 通道数
        dim = int(shape[1])  # 每个通道的数据轴数

        # 记录每条通道的均值和标准差
        channels_avg_and_std = []
        for i in xrange(0, channel_num):
            dataset_tem = dataset[i]
            avg_and_std = calculate_centre_point_avg_and_std(dataset_tem, dim, data_range)
            channels_avg_and_std.append(avg_and_std)
        return channels_avg_and_std

    else:
        return ['-nan', '-nan']


def calculate_centre_point_avg_and_std(dataset, dim, data_range=3):
    """
    计算一个二维正方形数据集中心点的均值和标准差
    :param dataset: 一个二维数据列表
    :param dim: 轴数
    :param data_range: 范围大小
    :return:
    """
    if len(dataset) != 0:
        # 获取切片的位置坐标
        num_start = int(dim / 2) - int(data_range / 2) - 1
        num_end = int(dim / 2) + int(data_range / 2)

        # 对数据表进行切片
        dataset = dataset[num_start:num_end, num_start:num_end]

        # 计算均值和标准差
        avg = np.mean(dataset)
        std = np.std(dataset)

        if avg == -999:
            return ['-nan', '-nan']
        else:
            return [avg, std]
    else:
        raise ValueError('value error： dataset')


def extract_lines(dataset, probe_count, probe_id):
    """
    提取探头号对应行的数据
    :param dataset: (np.ndarray)二维数据集
    :param probe_count: 探头数量
    :param probe_id: 探头号
    :return:
    """
    start = 0  # 开始行号
    end = start + probe_count  # 结束行号
    line_count = dataset.shape[0]  # 数据集总行数
    probe_id = int(probe_id) - 1
    dataset_new = []
    while start < line_count:
        # 取探元号对应行的数据
        line = dataset[start: end, :][probe_id]
        dataset_new.append(line)
        start += probe_count
        end += probe_count
    dataset_new = np.array(dataset_new)
    return dataset_new


def rolling_calculate_avg_std(dataset, rolling_lines):
    """
    对数组进行滚动计算，输出均值和标准差的列表
    :param dataset: (np.ndarray)二维数据集
    :param rolling_lines: 每次滚动的行数
    :return: (np.ndarray)
    """
    line_before = rolling_lines / 2  # 本行数据的前
    line_after = rolling_lines - (rolling_lines / 2)  # 本行数据后
    line_count = dataset.shape[0]  # 数据集的总行数
    # 滚动处理
    avg_std_list = []
    for i in xrange(0, line_count):
        start = i - line_before + 1  # 开始的行号
        start = start if start >= 0 else 0
        end = i + line_after + 1  # 结束的行号
        end = end if end <= line_count else line_count

        tem_dataset = dataset[start: end, :]
        avg = np.mean(tem_dataset)  # 计算均值
        std = np.std(tem_dataset)  # 计算标准差
        avg_std_list.append([avg, std])
    avg_std_list = np.array(avg_std_list)
    return avg_std_list
