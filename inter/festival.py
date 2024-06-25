import datetime
import holidays


def get_fifth_day_around_lunar_new_year(year):
    cn_holidays = holidays.China(years=year)
    lunar_new_year_dates = [date for date, name in cn_holidays.items() if "春节" in name]
    if not lunar_new_year_dates:
        return None, None
    start_date = lunar_new_year_dates[0]

    # 计算前五天和后五天的第五天的日期
    fifth_day_before = (start_date - datetime.timedelta(days=5)).strftime('%Y%m%d')
    fifth_day_after = (start_date + datetime.timedelta(days=5)).strftime('%Y%m%d')
    return fifth_day_before, fifth_day_after


def get_fifth_day_around_dragon_boat_festival(year):
    cn_holidays = holidays.China(years=year)
    dragon_boat_festival_dates = [date for date, name in cn_holidays.items() if "端午节" in name]
    if not dragon_boat_festival_dates:
        return None, None
    start_date = dragon_boat_festival_dates[0]

    # 计算前五天和后五天的第五天的日期
    fifth_day_before = (start_date - datetime.timedelta(days=5)).strftime('%Y%m%d')
    fifth_day_after = (start_date + datetime.timedelta(days=5)).strftime('%Y%m%d')
    return fifth_day_before, fifth_day_after


# 示例
year = input()
year = int(year)
lunar_new_year_before, lunar_new_year_after = get_fifth_day_around_lunar_new_year(year)
dragon_boat_before, dragon_boat_after = get_fifth_day_around_dragon_boat_festival(year)

print("春节前第五天的日期是：", lunar_new_year_before)
print("春节后第五天的日期是：", lunar_new_year_after)
print("端午节前第五天的日期是：", dragon_boat_before)
print("端午节后第五天的日期是：", dragon_boat_after)

