import os
import tkinter as tk
from PIL import Image, ImageTk
import time
from selenium import webdriver
from typing import List
import requests
from jsonpath import jsonpath
import holidays
import datetime
from tkinter import ttk, messagebox, simpledialog
import tkinter.scrolledtext as scrolledtext
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import threading
from chat_client2 import start_client
import websocket
import json
import _thread as thread
import base64
import datetime
import hashlib
import hmac
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time
from time import mktime
import ssl
from tkinter import PhotoImage





# def spider(n):
#     from selenium import webdriver
#     driver = webdriver.Edge()
#     num = '{:0>6d}'.format(n)
#     driver.get("http:data.eastmoney.com/stockdata/" + num + ".html")
#     driver.set_window_size(200, 400)
#     driver.execute_script('window.scrollBy(800,650)')
#     title = driver.title.split("_", 1)[0]
#     screenshot_path = f"D:/{num}{title}.png"
#     driver.get_screenshot_as_file(screenshot_path)
#     driver.quit()
#     return screenshot_path


ACCOUNT_FILE = "accounts.json"

# 初始化账户数据文件
def initialize_account_file():
    if not os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "w") as file:
            json.dump({}, file)

# 读取账户数据
def read_accounts():
    with open(ACCOUNT_FILE, "r") as file:
        return json.load(file)

# 保存账户数据
def save_accounts(accounts):
    with open(ACCOUNT_FILE, "w") as file:
        json.dump(accounts, file)

# 登录界面
def login_window():
    def login():
        accounts = read_accounts()
        username = username_entry.get()
        password = password_entry.get()
        if username in accounts and accounts[username] == password:
            messagebox.showinfo("登录成功", f"欢迎您，{username}！")
            root.destroy()
            main_window()  # 登录成功后进入主程序
        else:
            messagebox.showerror("登录失败", "用户名或密码错误！")

    def open_register_window():
        root.destroy()
        register_window()

    root = tk.Tk()
    root.title("登录")
    root.geometry("400x300")

    # 背景图片
    bg_image = Image.open("background.jpg")  # 替换为你的背景图片路径
    bg_image = bg_image.resize((400, 300), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # 使用 ttk 样式美化
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=6)
    style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0", padding=5)
    style.configure("TEntry", font=("Helvetica", 12))

    # 登录框
    login_frame = ttk.Frame(root, padding="20")
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    ttk.Label(login_frame, text="用户名：").grid(row=0, column=0, pady=10, sticky=tk.E)
    username_entry = ttk.Entry(login_frame, width=25)
    username_entry.grid(row=0, column=1, pady=10)

    ttk.Label(login_frame, text="密码：").grid(row=1, column=0, pady=10, sticky=tk.E)
    password_entry = ttk.Entry(login_frame, show="*", width=25)
    password_entry.grid(row=1, column=1, pady=10)

    login_button = ttk.Button(login_frame, text="登录", command=login, width=10)
    login_button.grid(row=2, column=0, pady=10)

    register_button = ttk.Button(login_frame, text="注册", command=open_register_window, width=10)
    register_button.grid(row=2, column=1, pady=10)

    root.mainloop()

# 注册界面
def register_window():
    def register():
        accounts = read_accounts()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if username in accounts:
            messagebox.showerror("注册失败", "用户名已存在！")
        elif password != confirm_password:
            messagebox.showerror("注册失败", "两次密码输入不一致！")
        else:
            accounts[username] = password
            save_accounts(accounts)
            messagebox.showinfo("注册成功", "注册成功，请返回登录界面！")
            root.destroy()
            login_window()

    root = tk.Tk()
    root.title("注册")
    root.geometry("400x350")

    # 背景图片
    bg_image = Image.open("background.jpg")  # 替换为你的背景图片路径
    bg_image = bg_image.resize((400, 350), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # 使用 ttk 样式美化
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=6)
    style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0", padding=5)
    style.configure("TEntry", font=("Helvetica", 12))

    # 注册框
    register_frame = ttk.Frame(root, padding="20")
    register_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    ttk.Label(register_frame, text="用户名：").grid(row=0, column=0, pady=10, sticky=tk.E)
    username_entry = ttk.Entry(register_frame, width=25)
    username_entry.grid(row=0, column=1, pady=10)

    ttk.Label(register_frame, text="密码：").grid(row=1, column=0, pady=10, sticky=tk.E)
    password_entry = ttk.Entry(register_frame, show="*", width=25)
    password_entry.grid(row=1, column=1, pady=10)

    ttk.Label(register_frame, text="确认密码：").grid(row=2, column=0, pady=10, sticky=tk.E)
    confirm_password_entry = ttk.Entry(register_frame, show="*", width=25)
    confirm_password_entry.grid(row=2, column=1, pady=10)

    register_button = ttk.Button(register_frame, text="注册", command=register, width=10)
    register_button.grid(row=3, column=0, pady=10)

    back_button = ttk.Button(register_frame, text="返回登录", command=lambda: [root.destroy(), login_window()], width=10)
    back_button.grid(row=3, column=1, pady=10)

    root.mainloop()

def spider_batch(a,b):
    driver = webdriver.Edge()
    for i in range(a, b):
        try:
            num = '{:0>6d}'.format(i)
            #补全股票代码
            driver.get("http:data.eastmoney.com/stockdata/" + num + ".html")
            driver.set_window_size(200,400)
            driver.execute_script('window.scrollBy(800,650)')
            title = driver.title
            title = title.split("_", 1)[0]
            if len(title)>10:
                continue
            driver.get_screenshot_as_file("D:" + num + title+ ".png")

        except:
            continue

time1=time.localtime(time.time())
now1=time.strftime("%Y/%m/%d %H:%M:%S",time1)


def time_count():
    print(now1)
    time2=time.localtime(time.time())
    now2=time.strftime("%Y/%m/%d %H:%M:%S",time2)
    #按年月日 小时分钟秒格式 结束时间
    print(now2)
class CustomedSession(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', 60)
        return super(CustomedSession, self).request(*args, **kwargs)


session = CustomedSession()
adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=5)
session.mount('http://', adapter)
session.mount('https://', adapter)

# 请求地址
QEURY_URL = 'http://push2his.eastmoney.com/api/qt/stock/kline/get'
# HTTP 请求头
EASTMONEY_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
}

"""
获取单只股票的历史K线数据
"""




def get_k_history_data(
    stock_codes: str,
    beg: str = '19000101',
    end: str = '20500101',
    klt: int = 101,
    fqt: int = 1,
):
    session = requests.Session()  # 假设session已经被正确设置

    try:
        secid = f'0.{stock_codes}' if stock_codes[0] != '6' else f'1.{stock_codes}'

        fields = "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
        params = {
            'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
            'fields2': fields,
            'beg': beg,
            'end': end,
            'rtntype': '6',
            'secid': secid,
            'klt': str(klt),
            'fqt': str(fqt),
        }

        data_list = []
        day_shift = 0
        max_tries = 100

        while not data_list and day_shift < max_tries:
            json_response = session.get(QEURY_URL, headers=EASTMONEY_REQUEST_HEADERS, params=params, verify=False).json()
            klines = jsonpath(json_response, '$..klines[:]')

            if klines:
                name = json_response.get('data', {}).get('name', '未知股票')
                for kline in klines:
                    time, open, close, high, low, vol, quota, mm, change, range, tun = kline.split(',')
                    line_str = f'"开盘"{open},"收盘"{close},"最高"{high},"最低"{low},"成交量"{vol},"成交额"{quota},"振幅"{mm},"涨跌幅"{change},"涨跌额"{range},换手率{tun}'
                    data_list.append({'股票代码': stock_codes, '股票名称': name, '时间': time, '股票信息': line_str})
            else:
                day_shift += 1  # 试图获取前一天或后一天的数据
                new_beg = datetime.strptime(beg, '%Y%m%d') + timedelta(days=day_shift)
                new_end = datetime.strptime(end, '%Y%m%d') + timedelta(days=day_shift)
                params['beg'] = new_beg.strftime('%Y%m%d')
                params['end'] = new_end.strftime('%Y%m%d')

        return data_list
    except Exception as e:
        print('get_k_history_data error-----------------------', str(e))
        return []

def get_fifth_day_around_lunar_new_year(year):
    cn_holidays = holidays.China(years=year)
    lunar_new_year_dates = [date for date, name in cn_holidays.items() if "春节" in name]
    if not lunar_new_year_dates:
        return None, None
    start_date = lunar_new_year_dates[0]


    fifth_day_before = (start_date - timedelta(days=10)).strftime('%Y%m%d')
    fifth_day_after = (start_date + timedelta(days=10)).strftime('%Y%m%d')
    return fifth_day_before, fifth_day_after


def get_fifth_day_around_dragon_boat_festival(year):
    cn_holidays = holidays.China(years=year)
    dragon_boat_festival_dates = [date for date, name in cn_holidays.items() if "端午节" in name]
    if not dragon_boat_festival_dates:
        return None, None
    start_date = dragon_boat_festival_dates[0]

    # 计算前五天和后五天的第五天的日期
    fifth_day_before = (start_date - timedelta(days=10)).strftime('%Y%m%d')
    fifth_day_after = (start_date + timedelta(days=10)).strftime('%Y%m%d')
    return fifth_day_before, fifth_day_after

def get_dragon_boat_festival_x(year,x):
    cn_holidays = holidays.China(years=year)
    dragon_boat_festival_dates = [date for date, name in cn_holidays.items() if "端午节" in name]
    if not dragon_boat_festival_dates:
        return None, None
    start_date = dragon_boat_festival_dates[0]

    x_after = (start_date + datetime.timedelta(days=x)).strftime('%Y%m%d')
    return x_after

def get_lunar_new_year_x(year, x):
    try:
        cn_holidays = holidays.China(years=int(year))
        lunar_new_year_dates = [date for date, name in cn_holidays.items() if "春节" in name]
        if lunar_new_year_dates:
            start_date = lunar_new_year_dates[0]
            x_date = (start_date + timedelta(days=x)).strftime('%Y%m%d')
            return x_date
        else:
            return "未知日期"
    except Exception as e:
        print(f"获取春节日期时发生错误: {e}")
        return "未知日期"




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

        stock_info_parts = item['股票信息'].split(',')
        open_price = next(part.split('开盘')[1] for part in stock_info_parts if '开盘' in part)
        open_prices.append(open_price.strip('"'))
        print(open_prices)
        print(names)
        print(times)
        print(codes)

    return codes, names, open_prices, times




def main_window():
    root = tk.Tk()
    root.geometry('981x676')
    root.resizable(False, False)
    root.title("股票信息处理系统")
    root.configure(bg="#f5f5f5")


    # 操作选择按钮
    root.grid_columnconfigure(0, weight=1)  # 主体内容宽度随窗口调整
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_columnconfigure(4, weight=1)
    root.grid_rowconfigure(1, weight=1)




    # def open_chat_program():
    #     # 创建新的窗口用于 AI 聊天程序
    #     chat_window = tk.Toplevel(root)
    #     chat_app = ChatApp(chat_window)  # 初始化聊天程序
    #     chat_window.mainloop()

    def handle_action():
        # 进行精确搜索
        n = simpledialog.askinteger("输入", "请输入您要搜索的股票代号：")
        if n is None:
            return  # 如果用户取消输入，则直接退出函数
        begin = simpledialog.askstring("输入", "请输入您关心的开始日期：")
        if not begin:
            messagebox.showerror("错误", "开始日期不能为空！")
            return
        over = simpledialog.askstring("输入", "请输入您关心的结束日期：")
        if not over:
            messagebox.showerror("错误", "结束日期不能为空！")
            return

        # 获取股票数据
        try:
            data = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin, end=over)
            if not data:
                messagebox.showinfo("提示", "未找到符合条件的数据！")
                return

            for item in data:
                txt.insert(tk.END, f"{item['股票代码']} {item['股票名称']} {item['时间']} {item['股票信息']}\n")
        except Exception as e:
            messagebox.showerror("错误", f"获取数据时发生错误：{str(e)}")


    def show_data_in_treeview(data):
        # 创建Treeview组件
        tree = ttk.Treeview(root)
        tree["columns"] = ("股票序号", "股票名称", "节日当天", "节日后十天", "升跌幅度1", "节日后十五天", "升跌幅度2")
        tree.column("#0", width=0, stretch=tk.NO)
        for col in tree["columns"]:
            tree.column(col, width=120)
            tree.heading(col, text=col)

        # 添加数据到Treeview
        for row in data:
            tree.insert("", "end", values=row)

        tree.grid(column=0, row=2, columnspan=4, sticky='nsew')

    def show_data_in_treeview_2(data):
        # 确保Treeview窗口只打开一次
        if 'treeview_window' not in globals():
            global treeview_window
            treeview_window = tk.Toplevel()
            treeview_window.title("全年节日盈亏数据展示")

        # 创建 Treeview 组件
        tree = ttk.Treeview(treeview_window)

        # 定义列
        tree['columns'] = ("股票代码", "股票名称", "年份", "节日十天后总体盈亏", "节日十五天后总体盈亏")

        # 格式化列
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("股票代码", anchor=tk.W, width=100)
        tree.column("股票名称", anchor=tk.W, width=200)
        tree.column("年份", anchor=tk.CENTER, width=100)
        tree.column("节日十天后总体盈亏", anchor=tk.E, width=150)
        tree.column("节日十五天后总体盈亏", anchor=tk.E, width=150)

        # 创建列标题
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("股票代码", text="股票代码", anchor=tk.W)
        tree.heading("股票名称", text="股票名称", anchor=tk.W)
        tree.heading("年份", text="年份", anchor=tk.CENTER)
        tree.heading("节日十天后总体盈亏", text="节日十天后总体盈亏", anchor=tk.E)
        tree.heading("节日十五天后总体盈亏", text="节日十五天后总体盈亏", anchor=tk.E)

        # 插入数据
        for row in data:
            tree.insert("", tk.END, values=row)

        tree.pack(expand=True, fill='both')

        # 显示窗口
        treeview_window.mainloop()


    def festival_data():
        n = simpledialog.askinteger("节日前后调查", "请输入您要搜索的股票代号：                ")

        year = simpledialog.askstring("年份", "请输入您感兴趣的年份(例：2023)：               ")
        festival = simpledialog.askstring("节日", "请输入您感兴趣的节日\n1.元旦\n2.春节\n3.劳动\n4.国庆\n5.端午              " )
        year = int(year)
        lunar_new_year_before, lunar_new_year_after = get_fifth_day_around_lunar_new_year(year)
        dragon_boat_before, dragon_boat_after = get_fifth_day_around_dragon_boat_festival(year)
        if festival == '1':
            year = int(year)
            year -= 1
            begin = f"{year}1227"
            year = int(year)
            year += 1
            over = f"{year}0106"
            data = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin, end=over)
            for item in data:
                txt.insert(tk.END, f"{item['股票代码']} {item['股票名称']} {item['时间']} {item['股票信息']}\n")
        if festival == '2':
            begin = lunar_new_year_before
            over = lunar_new_year_after
            print(begin, over)
            data = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin, end=over)
            for item in data:
                txt.insert(tk.END, f"{item['股票代码']} {item['股票名称']} {item['时间']} {item['股票信息']}\n")
        if festival == '3':
            begin = f"{year}0501"
            over = f"{year}0506"
            data = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin, end=over)
            for item in data:
                txt.insert(tk.END, f"{item['股票代码']} {item['股票名称']} {item['时间']} {item['股票信息']}\n")
        if festival == '4':
            begin = f"{year}1001"
            over = f"{year}1006"
            data = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin, end=over)
            for item in data:
                txt.insert(tk.END, f"{item['股票代码']} {item['股票名称']} {item['时间']} {item['股票信息']}\n")
        if festival == '5':

            begin = dragon_boat_before
            over = dragon_boat_after
            data = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin, end=over)
            for item in data:
                txt.insert(tk.END, f"{item['股票代码']} {item['股票名称']} {item['时间']} {item['股票信息']}\n")


    def annual_profit_analysis():
        stock_code = simpledialog.askstring("输入", "请输入股票代号：")
        if not stock_code:
            return


        year_window = tk.Toplevel()
        year_window.title("选择年份")
        year_window.geometry("300x700")

        # 可选择的年份列表
        years = [str(year) for year in range(2000, 2025)]


        # 创建多选框
        vars = []
        for year in years:
            var = tk.IntVar()
            chk = tk.Checkbutton(year_window, text=year, variable=var)
            chk.pack(anchor=tk.W)
            vars.append((year, var))

        def submit():
            selected_years = []
            selected_years = [year for year, var in vars if var.get() == 1]
            if len(selected_years) > 4:
                messagebox.showerror("错误", "最多只能选择四个年份")
                return
            calculate_yearly_profit(stock_code, selected_years)
            year_window.destroy()

        submit_btn = tk.Button(year_window, text="提交", command=submit)
        submit_btn.pack()

        year_window.mainloop()

    def calculate_yearly_profit(stock_code, years):
        print("处理的年份列表:", years)
        results = []  # 收集所有年份的结果，以便一次性显示

        for year in years:
            try:
                festivals = {
                    '元旦': {'begin': f"{int(year) - 1}1230", 'end_10': f"{year}0110", 'end_15': f"{year}0116"},
                    '春节': {'begin': get_lunar_new_year_x(year, -2), 'end_10': get_lunar_new_year_x(year, 10),
                             'end_15': get_lunar_new_year_x(year, 16)},
                    '劳动节': {'begin': f"{year}0430", 'end_10': f"{year}0510", 'end_15': f"{year}0516"},
                    '国庆节': {'begin': f"{year}0927", 'end_10': f"{year}1010", 'end_15': f"{year}1016"}
                }
                print(f"年份 {year} 的节日数据:", festivals)

                total_gain_10 = 0
                total_gain_15 = 0
                stock_name = "未知股票"  # 默认值，应通过API获取

                padded_stock_code = stock_code.zfill(6)
                for fest, dates in festivals.items():
                    if None in dates.values():  # 检查是否有无效的日期
                        continue  # 跳过无效的节日数据处理

                    data_begin = get_k_history_data(stock_codes=padded_stock_code, beg=dates['begin'],
                                                    end=dates['begin'])
                    data_10 = get_k_history_data(stock_codes=padded_stock_code, beg=dates['end_10'],
                                                 end=dates['end_10'])
                    data_15 = get_k_history_data(stock_codes=padded_stock_code, beg=dates['end_15'],
                                                 end=dates['end_15'])

                    print(data_begin, data_10, data_15)

                    a1, b1, c1, _ = extract_separate_lists(data_begin)
                    _, _, c2, _ = extract_separate_lists(data_10)
                    _, _, c3, _ = extract_separate_lists(data_15)

                    if c1 and c2 and c3:
                        gains_10_days = (float(c2[0]) - float(c1[0])) / float(c1[0])
                        gains_15_days = (float(c3[0]) - float(c1[0])) / float(c1[0])

                        total_gain_10 += gains_10_days
                        total_gain_15 += gains_15_days
                        if b1:
                            stock_name = b1[0]


                results.append((padded_stock_code, stock_name, year, total_gain_10, total_gain_15))
            except Exception as e:
                print(f"处理年份 {year} 时发生错误:", e)
                continue

        if results:
            show_yearly_profit(results)

    def show_yearly_profit(data):
        if 'profit_window' not in globals():
            global profit_window
            profit_window = tk.Toplevel()
            profit_window.title("年度盈亏分析")

        tree = ttk.Treeview(profit_window)
        tree['columns'] = ("股票代码", "股票名称", "年份", "十天后盈亏", "十五天后盈亏")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("股票代码", anchor=tk.W, width=100)
        tree.column("股票名称", anchor=tk.W, width=200)
        tree.column("年份", anchor=tk.CENTER, width=100)
        tree.column("十天后盈亏", anchor=tk.E, width=120)
        tree.column("十五天后盈亏", anchor=tk.E, width=120)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("股票代码", text="股票代码", anchor=tk.W)
        tree.heading("股票名称", text="股票名称", anchor=tk.W)
        tree.heading("年份", text="年份", anchor=tk.CENTER)
        tree.heading("十天后盈亏", text="十天后盈亏", anchor=tk.E)
        tree.heading("十五天后盈亏", text="十五天后盈亏", anchor=tk.E)

        for row in data:
            tree.insert("", tk.END, values=row)

        tree.pack(expand=True, fill='both')

        plot_button = tk.Button(profit_window, text="显示盈亏折线图", command=lambda: plot_profit_chart(data))
        plot_button.pack()

        profit_window.mainloop()

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


    def plot_profit_chart(data):
        new_window = tk.Toplevel()
        new_window.title("Annual Profit and Loss Chart")


        fig, ax = plt.subplots(figsize=(10, 5))
        years = [row[2] for row in data]  # 获取年份
        gains_10_days = [row[3] for row in data]  # 获取十天后的盈亏
        gains_15_days = [row[4] for row in data]  # 获取十五天后的盈亏

        ax.plot(years, gains_10_days, label='Profit and loss after 10 days', marker='o', color='b')
        ax.plot(years, gains_15_days, label='Profit and loss after 15 days', marker='o', color='r')
        ax.set_title("Annual Profit and Loss Chart")
        ax.set_xlabel("year")
        ax.set_ylabel("waxing and waning")
        ax.legend()
        ax.grid(True)


        canvas = FigureCanvasTkAgg(fig, master=new_window)  # 将fig与新窗口关联
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)  # 将matplotlib的画布嵌入到Tkinter

        new_window.mainloop()


    def festival_change():
        gains_10_days = 0
        gains_15_days = 0

        # 存储每个节日后10天和15天的总盈亏
        total_gain_10 = 0
        total_gain_15 = 0

        n = simpledialog.askinteger("节假日股票开盘对比", "请输入您要搜索的股票代号：                ")
        year = simpledialog.askstring("年份", "请输入您感兴趣的年份(例：2023)：               ")
        festival = simpledialog.askstring("节日",
                                          "请输入您感兴趣的节日\n1.元旦\n2.春节\n3.劳动\n4.国庆\n5.全年节日的盈亏            ")
        lunar_new_year_before, lunar_new_year_after = get_fifth_day_around_lunar_new_year(year)
        dragon_boat_before, dragon_boat_after = get_fifth_day_around_dragon_boat_festival(year)
        year = int(year)

        if festival == '1':
            year = int(year)
            year -= 1
            begin_1 = f"{year}1230"
            year = int(year)
            year += 1
            over_1 = f"{year}0102"
            begin_2 = f"{year}0110"
            over_2 = f"{year}0110"
            begin_3 = f"{year}0116"
            over_3 = f"{year}0116"
            data_1 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_1, end=over_1)
            data_2 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_2, end=over_2)
            data_3 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_3, end=over_3)
            a1, b1, c1, d1 = extract_separate_lists(data_1)
            a2, b2, c2, d2 = extract_separate_lists(data_2)
            a3, b3, c3, d3 = extract_separate_lists(data_3)


            if len(c1) == len(c2) == len(c3):
                table_data = list(zip(
                    a1, b1, c1, c2,
                    [(float(c2[i]) - float(c1[i])) / float(c1[i]) for i in range(len(c1))],
                    c3,
                    [(float(c3[i]) - float(c1[i])) / float(c1[i]) for i in range(len(c1))]
                ))
                show_data_in_treeview(table_data)
            else:
                messagebox.showerror("错误", "数据长度不一致，无法计算升跌幅度。")


        if festival == '2':
            begin_1 = get_lunar_new_year_x(year,-2)
            over_1 = get_lunar_new_year_x(year,-2)
            begin_2 = get_lunar_new_year_x(year,10)
            over_2 = get_lunar_new_year_x(year,10)
            begin_3 = get_lunar_new_year_x(year,16)
            over_3 = get_lunar_new_year_x(year,16)
            data_1 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_1, end=over_1)
            data_2 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_2, end=over_2)
            data_3 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_3, end=over_3)
            a1, b1, c1, d1 = extract_separate_lists(data_1)
            a2, b2, c2, d2 = extract_separate_lists(data_2)
            a3, b3, c3, d3 = extract_separate_lists(data_3)

            # 假设你已经提供了创建表格所需的所有数据
            if len(c1) == len(c2) == len(c3):
                table_data = list(zip(
                    a1, b1, c1, c2,
                    [(float(c2[i]) - float(c1[i])) / float(c1[i]) for i in range(len(c1))],
                    c3,
                    [(float(c3[i]) - float(c1[i])) / float(c1[i]) for i in range(len(c1))]
                ))
                show_data_in_treeview(table_data)
            else:
                messagebox.showerror("错误", "数据长度不一致，无法计算升跌幅度。")

        if festival == '3':
            begin_1 = f"{year}0430"
            over_1 = f"{year}0430"
            begin_2 = f"{year}0510"
            over_2 = f"{year}0510"
            begin_3 = f"{year}0516"
            over_3 = f"{year}0516"
            # 假设 get_k_history_data 能够返回期望的数据格式
            data_1 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_1, end=over_1)
            data_2 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_2, end=over_2)
            data_3 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_3, end=over_3)
            a1, b1, c1, d1 = extract_separate_lists(data_1)
            a2, b2, c2, d2 = extract_separate_lists(data_2)
            a3, b3, c3, d3 = extract_separate_lists(data_3)

            # 假设你已经提供了创建表格所需的所有数据
            if len(c1) == len(c2) == len(c3):
                table_data = list(zip(
                    a1, b1, c1, c2,
                    [(float(c2[i]) - float(c1[i])) / float(c1[i]) for i in range(len(c1))],
                    c3,
                    [(float(c3[i]) - float(c1[i])) / float(c1[i]) for i in range(len(c1))]
                ))
                show_data_in_treeview(table_data)
            else:
                messagebox.showerror("错误", "数据长度不一致，无法计算升跌幅度。")

        if festival == '4':
            begin_1 = f"{year}0927"
            over_1 = f"{year}0927"
            begin_2 = f"{year}1010"
            over_2 = f"{year}1010"
            begin_3 = f"{year}1016"
            over_3 = f"{year}1016"
            # 假设 get_k_history_data 能够返回期望的数据格式
            data_1 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_1, end=over_1)
            data_2 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_2, end=over_2)
            data_3 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin_3, end=over_3)
            a1, b1, c1, d1 = extract_separate_lists(data_1)
            a2, b2, c2, d2 = extract_separate_lists(data_2)
            a3, b3, c3, d3 = extract_separate_lists(data_3)

            # 假设你已经提供了创建表格所需的所有数据
            if len(c1) == len(c2) == len(c3):
                table_data = list(zip(
                    a1, b1, c1, c2,
                    [(float(c2[i]) - float(c1[i])) / float(c1[i]) for i in range(len(c1))],
                    c3,
                    [(float(c3[i]) - float(c1[i])) / float(c1[i]) for i in range(len(c1))]
                ))
                show_data_in_treeview(table_data)
            else:
                messagebox.showerror("错误", "数据长度不一致，无法计算升跌幅度。")

        if festival == '5':
            festivals = {
                '元旦': {'begin': f"{year - 1}1230", 'end_10': f"{year}0110", 'end_15': f"{year}0116"},
                '春节': {'begin': get_lunar_new_year_x(year, -2), 'end_10': get_lunar_new_year_x(year, 10),
                         'end_15': get_lunar_new_year_x(year, 16)},
                '劳动节': {'begin': f"{year}0430", 'end_10': f"{year}0510", 'end_15': f"{year}0516"},
                '国庆节': {'begin': f"{year}0927", 'end_10': f"{year}1010", 'end_15': f"{year}1016"}
            }

            for fest, dates in festivals.items():
                data_begin = get_k_history_data(stock_codes=f'{n:0>6d}', beg=dates['begin'], end=dates['begin'])
                data_10 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=dates['end_10'], end=dates['end_10'])
                data_15 = get_k_history_data(stock_codes=f'{n:0>6d}', beg=dates['end_15'], end=dates['end_15'])

                a1, b1, c1, _ = extract_separate_lists(data_begin)
                _, _, c2, _ = extract_separate_lists(data_10)
                _, _, c3, _ = extract_separate_lists(data_15)

                if c1 and c2 and c3:
                    gains_10_days = (float(c2[0]) - float(c1[0])) / float(c1[0])
                    gains_15_days = (float(c3[0]) - float(c1[0])) / float(c1[0])

                    total_gain_10 += gains_10_days
                    total_gain_15 += gains_15_days

            # 使用第一个查询的股票名称 b1[0]
            show_data_in_treeview_2([(n, b1[0],year, total_gain_10, total_gain_15)])



##################################################################################################################

    # 加载背景图片
    background_image = Image.open("background.jpg")
    background_photo = ImageTk.PhotoImage(background_image.resize((981, 676)))
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # 使用 ttk 样式进行美化
    style = ttk.Style()
    style.configure("TFrame", background="#f5f5f5")
    style.configure("TButton", font=("Helvetica", 12), padding=6, background="#008000", foreground="black")
    style.map("TButton", background=[('active', '#45a049')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    # 标题标签
    title_label = tk.Label(root, text="股票信息处理系统", font=("Arial", 24, "bold"), bg="#f5f5f5", fg="#333333")
    title_label.grid(column=0, row=0, columnspan=5, pady=(20, 10), sticky=tk.W)  # 左对齐标题

    # # 加载按钮图标
    try:
        button_icon = PhotoImage(file="ui.png")  # 替换为你的图标文件路径
    except Exception as e:
        print(f"无法加载图标: {e}")
        button_icon = None

    # 添加标题右边的小按钮
    # icon_button = ttk.Button(root, image=button_icon, command=lambda: print("按钮功能暂时为空"))  # 暂时空功能
    # icon_button.place(x=930, y=10)  # 绝对定位，调整到标题右边的位置

    icon_button = ttk.Button(root, image=button_icon, command=lambda: threading.Thread(target=start_client).start())
    icon_button.place(x=930, y=10)
    # 滚动文本框用于显示数据
    txt = scrolledtext.ScrolledText(root, width=100, height=20, font=("Helvetica", 12), bg='#395961',
                                    highlightthickness=0, bd=0)
    txt.grid(column=0, row=2, columnspan=5, padx=20, pady=(10, 20))

    # 按钮容器框架
    button_frame = ttk.Frame(root, style="TFrame")
    button_frame.grid(column=0, row=1, columnspan=5, pady=(1, 1))

    # 常规操作按钮
    action_button_1 = ttk.Button(button_frame, text="常规操作", command=handle_action, style="TButton")
    action_button_1.grid(column=0, row=0, padx=(5, 10), pady=5)

    # 节日前后调查按钮
    action_button_2 = ttk.Button(button_frame, text="节日前后调查", command=festival_data, style="TButton")
    action_button_2.grid(column=1, row=0, padx=(5, 10), pady=5)

    # 年度收益图像分析按钮
    annual_profit_button = ttk.Button(button_frame, text="年度收益图像分析", command=annual_profit_analysis,
                                      style="TButton")
    annual_profit_button.grid(column=3, row=0, padx=(5, 10), pady=5)

    # AI建议按钮
    Ai_button = ttk.Button(button_frame, text="AI建议", command=ai_suggestion, style="TButton")
    Ai_button.grid(column=4, row=0, padx=(5, 10), pady=5)

    # 退出按钮
    quit_button = ttk.Button(button_frame, text="退出程序", command=root.destroy, style="TButton")
    quit_button.grid(column=5, row=0, padx=(5, 10), pady=5)

    root.mainloop()

class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    def create_url(self):
        now = datetime.datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        url = self.gpt_url + '?' + urlencode(v)
        return url


def on_message(ws, message, app):
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]

        # 将接收到的内容追加到缓冲区
        ws.buffer += content

        # 检查是否包含标点符号，决定是否更新 UI
        if any(punct in ws.buffer for punct in '.!?'):
            app.display_message(ws.buffer, "left")
            ws.buffer = ""  # 清空缓冲区

        if status == 2:  # 如果状态为完成
            if ws.buffer:
                app.display_message(ws.buffer, "left")
                ws.buffer = ""
            ws.close()

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    thread.start_new_thread(run, (ws,))

def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, query=ws.query, domain=ws.domain))
    ws.send(data)

def gen_params(appid, query, domain):
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234",
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 1,
                "max_tokens": 1024,
                "auditing": "default",
            }
        },
        "payload": {
            "message": {
                "text": [{"role": "user", "content": query}]
            }
        }
    }
    return data

def start_ws(appid, api_secret, api_key, gpt_url, domain, query, app):
    wsParam = Ws_Param(appid, api_key, api_secret, gpt_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()

    ws = websocket.WebSocketApp(
        wsUrl,
        on_message=lambda ws, message: on_message(ws, message, app),  # 传递 app 实例
        on_close=on_close,
        on_open=on_open
    )
    ws.appid = appid
    ws.query = query
    ws.domain = domain
    ws.buffer = ""  # 初始化缓冲区
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry('600x400')

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, width=80)
        self.entry.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10, side=tk.RIGHT)

    def send_message(self, event=None):
        message = self.entry.get()
        if message.strip():
            self.display_message(message, "right")
            self.entry.delete(0, tk.END)
            threading.Thread(target=start_ws, args=(
                "fdd4df16", "M2U5OWM2ZGRkZTllZjU1NTQ3YTUzMzg4",
                "e3c60f5ff9a8c948251062d4dbec4853",
                "wss://spark-api.xf-yun.com/v4.0/chat", "4.0Ultra", message, self  # 传递 ChatApp 实例
            )).start()

    def display_message(self, message, side):
        self.text_area.configure(state='normal')
        if side == "right":
            self.text_area.tag_configure("right", justify='right', wrap=tk.WORD)
            self.text_area.insert(tk.END, f"{message}\n\n", "right")
        else:
            self.text_area.tag_configure("left", justify='left', wrap=tk.WORD)
            self.text_area.insert(tk.END, f"{message}\n\n", "left")
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)
def ai_suggestion():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()



def show_image(path, master):
    if path:
        image = Image.open(path)
        image = image.resize((600, 400), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(master, image=photo)
        label.image = photo  # keep a reference!
        label.grid(column=4, row=1)






if __name__ == "__main__":
    initialize_account_file()
    login_window()
