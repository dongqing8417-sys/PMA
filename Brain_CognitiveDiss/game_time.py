from datetime import datetime, timedelta, time
import logging

# class Time:
#     def __init__(self):
#         # 初始化时间为今天6:00
#         now = datetime.now()
#         self.current_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
#         self.time_step = timedelta(minutes=15)
#
#     def advance_time(self):
#         """前进时间15分钟"""
#         self.current_time += self.time_step
#
#     def get_current_time(self):
#         """返回当前的datetime对象"""
#         return self.current_time
#
#     def get_date_nl(self):
#         """获取当前日期的自然语言格式"""
#         day_of_week = self.current_time.strftime('%A')
#         month_date_year = self.current_time.strftime("%b %d %Y")
#         date = f"{day_of_week} {month_date_year}"
#         return date
#
#     def get_time_nl(self):
#         """获取当前时间的自然语言格式"""
#         time = self.current_time.strftime('%I:%M %p').lower()
#         return time
#
#     def get_formatted_date_time(self):
#         """获取格式化后的日期时间字符串"""
#         date_in_nl = self.get_date_nl()
#         time_in_nl = self.get_time_nl()
#         formatted_date_time = f"{date_in_nl} {time_in_nl}"
#         return formatted_date_time
#
#     def get_date(self):
#         """返回当前的日期对象"""
#         return self.current_time.date()
#
#     def set_time(self, hour, minute):
#         """设置当前时间的小时和分钟"""
#         self.current_time = self.current_time.replace(hour=hour, minute=minute)
#
#     def set_date(self, year, month, day):
#         """设置当前的日期"""
#         self.current_time = self.current_time.replace(year=year, month=month, day=day)

class Time:
    def __init__(self):
        # 初始化时间为今天8:00
        now = datetime.now()
        self.current_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
        self.time_step = timedelta(minutes=30)

    def advance_time(self):
        """前进时间15分钟"""
        self.current_time += self.time_step

    def get_current_time(self):
        """返回当前的datetime对象"""
        return self.current_time

    def get_date_nl(self):
        date = self.current_time.strftime("%Y-%m-%d")
        return date

    def get_time_24h(self):
        """获取当前时间的24小时格式"""
        time = self.current_time.strftime('%H:%M')
        return time

    def get_formatted_date_time(self):
        """获取格式化后的日期时间字符串，使用24小时制"""
        date_in_nl = self.get_date_nl()
        time_in_24h = self.get_time_24h()
        formatted_date_time = f"{date_in_nl} {time_in_24h}"
        return formatted_date_time

    def get_date(self):
        """返回当前的日期对象"""
        return self.current_time.date()

    def get_date_str(self):
        """以 'YYYY-MM-DD' 格式返回当前日期的字符串"""
        return self.current_time.strftime('%Y-%m-%d')

    def set_time(self, new_time: time):
        """使用 time 对象设置当前时间的小时和分钟"""
        self.current_time = self.current_time.replace(hour=new_time.hour, minute=new_time.minute)


    def set_date(self, year, month, day):
        """设置当前的日期"""
        self.current_time = self.current_time.replace(year=year, month=month, day=day)

    def calculate_future_date(self, day: int):
        """根据 day 参数计算从当前日期起第 day 天的日期，返回 'YYYY-MM-DD' 格式字符串"""
        future_date = self.current_time + timedelta(days=day - 1)  # day=1 表示今天
        return future_date.strftime('%Y-%m-%d')



# print(t.get_date_nl())  # Tuesday Jul 23 2024
# print(t.get_time_nl())  # 06:00 am
# print(t.get_formatted_date_time())  # Tuesday Jul 23 2024 06:00 am
