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

def spider(n):
    from selenium import webdriver
    driver = webdriver.Edge()
    num = '{:0>6d}'.format(n)
    driver.get("http:data.eastmoney.com/stockdata/" + num + ".html")
    driver.set_window_size(200, 400)
    driver.execute_script('window.scrollBy(800,650)')
    title = driver.title.split("_", 1)[0]
    screenshot_path = f"D:/{num}{title}.png"
    driver.get_screenshot_as_file(screenshot_path)
    driver.quit()
    return screenshot_path


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
        stock_codes: str,  # 股票代码
        beg: str = '19000101',  # 开始日期，19000101，表示 1900年1月1日
        end: str = '20500101',  # 结束日期
        klt: int = 101,  # 行情之间的时间间隔 1、5、15、30、60分钟; 101:日; 102:周; 103:月
        fqt: int = 1,  # 复权方式，0 不复权 1 前复权 2 后复权
):
    try:
        # 生成东方财富专用的secid
        if stock_codes[:3] == '000':
            secid = f'1.{stock_codes}'
        elif stock_codes[:3] == '399':
            secid = f'0.{stock_codes}'

        if stock_codes[0] != '6':
            secid = f'0.{stock_codes}'
        else:
            secid = f'1.{stock_codes}'

        EASTMONEY_KLINE_FIELDS = {'f51': '日期', 'f52': '开盘', 'f53': '收盘', 'f54': '最高', 'f55': '最低',
                                  'f56': '成交量', 'f57': '成交额', 'f58': '振幅', 'f59': '涨跌幅', 'f60': '涨跌额',
                                  'f61': '换手率', }
        fields = list(EASTMONEY_KLINE_FIELDS.keys())
        fields2 = ",".join(fields)
        params = (
            ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
            ('fields2', fields2),
            ('beg', beg),
            ('end', end),
            ('rtntype', '6'),
            ('secid', secid),
            ('klt', f'{klt}'),
            ('fqt', f'{fqt}'),
        )
        code = secid.split('.')[-1]
        json_response = session.get(QEURY_URL, headers=EASTMONEY_REQUEST_HEADERS, params=params, verify=False).json()
        data_list = []
        klines: List[str] = jsonpath(json_response, '$..klines[:]')
        if not klines:
            return data_list

        name = json_response['data']['name']
        rows = [kline.split(',') for kline in klines]
        for row in rows:
            time, open, close, high, low, vol, quota, mm, change, range, tun = row
            line_str = f'"开盘"{open},"收盘"{close},"最高"{high},"最低"{low},"成交量"{vol},"成交额"{quota},"振幅"{mm},"涨跌幅"{change},"涨跌额"{range},换手率{tun}'
            data_list.append({'股票代码': code, '股票名称': name, '时间': time, '股票信息': line_str})

        return data_list
    except Exception as e:
        print('get_k_history_data error-----------------------', str(e))
        return data_list

def get_fifth_day_around_lunar_new_year(year):
    cn_holidays = holidays.China(years=year)
    lunar_new_year_dates = [date for date, name in cn_holidays.items() if "春节" in name]
    if not lunar_new_year_dates:
        return None, None
    start_date = lunar_new_year_dates[0]

    # 计算前五天和后五天的第五天的日期
    fifth_day_before = (start_date - datetime.timedelta(days=10)).strftime('%Y%m%d')
    fifth_day_after = (start_date + datetime.timedelta(days=10)).strftime('%Y%m%d')
    return fifth_day_before, fifth_day_after


def get_fifth_day_around_dragon_boat_festival(year):
    cn_holidays = holidays.China(years=year)
    dragon_boat_festival_dates = [date for date, name in cn_holidays.items() if "端午节" in name]
    if not dragon_boat_festival_dates:
        return None, None
    start_date = dragon_boat_festival_dates[0]

    # 计算前五天和后五天的第五天的日期
    fifth_day_before = (start_date - datetime.timedelta(days=10)).strftime('%Y%m%d')
    fifth_day_after = (start_date + datetime.timedelta(days=10)).strftime('%Y%m%d')
    return fifth_day_before, fifth_day_after

def get_dragon_boat_festival_x(year,x):
    cn_holidays = holidays.China(years=year)
    dragon_boat_festival_dates = [date for date, name in cn_holidays.items() if "端午节" in name]
    if not dragon_boat_festival_dates:
        return None, None
    start_date = dragon_boat_festival_dates[0]

    x_after = (start_date + datetime.timedelta(days=x)).strftime('%Y%m%d')
    return x_after

def get_lunar_new_year_x(year,x):
    cn_holidays = holidays.China(years=year)
    lunar_new_year_dates = [date for date, name in cn_holidays.items() if "春节" in name]
    if not lunar_new_year_dates:
        return None, None
    start_date = lunar_new_year_dates[0]

    x_after = (start_date + datetime.timedelta(days=x)).strftime('%Y%m%d')
    return x_after




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
        print(open_prices)
        print(names)
        print(times)
        print(codes)

    return codes, names, open_prices, times




def main_window():
    root = tk.Tk()
    root.title("股票信息处理系统")
    root.geometry('1920x1080')

    # 添加滚动文本框用于显示数据
    txt = scrolledtext.ScrolledText(root, width=120, height=40)
    txt.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

    # 操作选择按钮
    def handle_action():
        action = messagebox.askquestion("常规操作", "是否批量截图？\nTips：如果是则截取给定范围的股票走势图，若为否则针对一个股票进行指定日期的分析\nyes（是）“批量处理”\nno（否）“精确搜索”")
        if action == 'yes':  # 用户选择“是”对应批量处理
            a = simpledialog.askinteger("输入", "请输入你要搜索的起点                 ")
            b = simpledialog.askinteger("输入", "请输入你要搜索的终点                 ")
            spider_batch(a, b, txt)
        else:  # 用户选择“否”对应精确搜索
            n = simpledialog.askinteger("输入", "请输入您要搜索的股票代号：                ")
            screenshot_path = spider(n)
            begin = simpledialog.askstring("输入", "请输入您关心的开始日期：               ")
            over = simpledialog.askstring("输入", "请输入您关心的结束日期：                ")
            data = get_k_history_data(stock_codes=f'{n:0>6d}', beg=begin, end=over)
            for item in data:
                txt.insert(tk.END, f"{item['股票代码']} {item['股票名称']} {item['时间']} {item['股票信息']}\n")
            show_image(screenshot_path, root)

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
        screenshot_path = spider(n)
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

        show_image(screenshot_path, root)

    def annual_profit_analysis():
        # 弹出输入股票代号的对话框
        stock_code = simpledialog.askstring("输入", "请输入股票代号：")
        if not stock_code:
            return

        # 选择年份的窗口
        year_window = tk.Toplevel()
        year_window.title("选择年份")
        year_window.geometry("300x700")

        # 可选择的年份列表
        years = [str(year) for year in range(2000, 2025)]
        selected_years = []

        # 创建多选框
        vars = []
        for year in years:
            var = tk.IntVar()
            chk = tk.Checkbutton(year_window, text=year, variable=var)
            chk.pack(anchor=tk.W)
            vars.append((year, var))

        def submit():
            selected_years = [year for year, var in vars if var.get() == 1]
            print(selected_years)
            if len(selected_years) > 4:
                messagebox.showerror("错误", "最多只能选择四个年份")
                return
            calculate_yearly_profit(stock_code, selected_years)
            year_window.destroy()

        submit_btn = tk.Button(year_window, text="提交", command=submit)
        submit_btn.pack()

        year_window.mainloop()

    def calculate_yearly_profit(stock_code, years):
        for year in years:
            festivals = {
                '元旦': {'begin': f"{int(year) - 1}1230", 'end_10': f"{year}0110", 'end_15': f"{year}0116"},
                '春节': {'begin': get_lunar_new_year_x(year, -2), 'end_10': get_lunar_new_year_x(year, 10),
                         'end_15': get_lunar_new_year_x(year, 16)},
                '劳动节': {'begin': f"{year}0430", 'end_10': f"{year}0510", 'end_15': f"{year}0516"},
                '国庆节': {'begin': f"{year}0927", 'end_10': f"{year}1010", 'end_15': f"{year}1016"}
            }
            print(festivals)

            total_gain_10 = 0
            total_gain_15 = 0


            for fest, dates in festivals.items():
                padded_stock_code = stock_code.zfill(6)
                data_begin = get_k_history_data(stock_codes=padded_stock_code, beg=dates['begin'], end=dates['begin'])
                data_10 = get_k_history_data(stock_codes=padded_stock_code, beg=dates['end_10'], end=dates['end_10'])
                data_15 = get_k_history_data(stock_codes=padded_stock_code, beg=dates['end_15'], end=dates['end_15'])
                print(data_begin, data_10, data_15)

                a1, b1, c1, _ = extract_separate_lists(data_begin)
                _, _, c2, _ = extract_separate_lists(data_10)
                _, _, c3, _ = extract_separate_lists(data_15)

                if c1 and c2 and c3:
                    gains_10_days = (float(c2[0]) - float(c1[0])) / float(c1[0])
                    gains_15_days = (float(c3[0]) - float(c1[0])) / float(c1[0])

                    total_gain_10 += gains_10_days
                    total_gain_15 += gains_15_days

            # 显示结果
            show_yearly_profit([(padded_stock_code, b1[0], year, total_gain_10, total_gain_15)])

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
        profit_window.mainloop()


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


        if festival == '2':
            begin_1 = get_lunar_new_year_x(year,-2)
            over_1 = get_lunar_new_year_x(year,-2)
            begin_2 = get_lunar_new_year_x(year,10)
            over_2 = get_lunar_new_year_x(year,10)
            begin_3 = get_lunar_new_year_x(year,16)
            over_3 = get_lunar_new_year_x(year,16)
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










    action_button = tk.Button(root, text="常规操作", command=handle_action)
    action_button.grid(column=0, row=0, padx=10, pady=10)

    action_button = tk.Button(root, text="节日前后调查", command=festival_data)
    action_button.grid(column=1, row=0, padx=10, pady=10)

    # 退出按钮
    quit_button = tk.Button(root, text="退出程序", command=root.destroy)
    quit_button.grid(column=2, row=0, padx=10, pady=10)

    action_button = tk.Button(root, text="节假日股票开盘对比", command=festival_change)
    action_button.grid(column=3, row=0, padx=10)

    annual_profit_button = tk.Button(root, text="年度收益图像分析", command=annual_profit_analysis)
    annual_profit_button.grid(column=4, row=0, padx=10, pady=10)

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
    main_window()
