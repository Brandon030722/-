import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import time
from selenium import webdriver
from typing import List
import requests
from jsonpath import jsonpath
import holidays
import datetime

data_list = []
open=1
close=2
high =3
low= 4
vol=5
quota=6
mm=7
change=8
range=9
tun=10
code=11
name=12
time=13


line_str = f'"开盘"{open},"收盘"{close},"最高"{high},"最低"{low},"成交量"{vol},"成交额"{quota},"振幅"{mm},"涨跌幅"{change},"涨跌额"{range},换手率{tun}'
data_list.append({'股票代码': code, '股票名称': name, '时间': time, '股票信息': line_str})


def extract_separate_lists(data_list):
    # 初始化四个列表来分别存储每个字段的所有数据
    codes = []
    names = []
    open_prices = []
    times = []

    # 遍历原始数据列表中的每一项
    for item in data_list:
        # 提取股票代码和股票名称，并添加到相应的列表
        codes.append(item['股票代码'])
        names.append(item['股票名称'])
        times.append(item['时间'])

        # 从股票信息中提取开盘价格，并添加到列表
        # 先分割整个字符串
        stock_info_parts = item['股票信息'].split(',')
        # 寻找包含"开盘"的部分并提取数值
        open_price = next(part.split('开盘')[1] for part in stock_info_parts if '开盘' in part)
        open_prices.append(open_price.strip('"'))

    return codes, names, open_prices, times

print(data_list)

extract_separate_lists(data_list)
a,b,c,d=extract_separate_lists(data_list)
print(a)
print(b)
print(c)
print(d)