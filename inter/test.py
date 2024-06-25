import time
from selenium import webdriver




def spider(n):
    driver = webdriver.Edge()
    num = '{:0>6d}'.format(n)
    # 补全股票代码
    driver.get("http:data.eastmoney.com/stockdata/" + num + ".html")
    driver.set_window_size(200, 400)
    driver.execute_script('window.scrollBy(800,650)')
    title = driver.title
    title = title.split("_", 1)[0]

    driver.get_screenshot_as_file("D:" + num + title + ".png")


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
            #截图并保存到该路径下命名为
        except:
            continue

time1=time.localtime(time.time())
now1=time.strftime("%Y/%m/%d %H:%M:%S",time1)
#按年月日 小时分钟秒格式 开始时间

def time_count():
    print(now1)
    time2=time.localtime(time.time())
    now2=time.strftime("%Y/%m/%d %H:%M:%S",time2)
    #按年月日 小时分钟秒格式 结束时间
    print(now2)

if __name__ == '__main__':
    print("选择你要采取的方式：")
    print("1.批量处理 2.精确搜索")
    action = input("：")
    num = eval(action)
    if (num == 1):
        print("请输入你要搜索的起点")
        action = input("起点：")
        a = eval(action)
        print("请输入你要搜索的终点")
        action = input("终点：")
        b = eval(action)
        spider_batch(a, b)
    if (num == 2):
        print("请输入你要搜索的股票")
        action = input("你要搜索的股票代码：")
        n = eval(action)
        spider(n)
    time_count()



