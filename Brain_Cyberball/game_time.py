from datetime import datetime, timedelta, time
import logging

# class Time:
#     def __init__(self):
#         # 6:00
#         now = datetime.now()
#         self.current_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
#         self.time_step = timedelta(minutes=15)
#
#     def advance_time(self):
#         """15"""
#         self.current_time += self.time_step
#
#     def get_current_time(self):
#         """datetime"""
#         return self.current_time
#
#     def get_date_nl(self):
#         """"""
#         day_of_week = self.current_time.strftime('%A')
#         month_date_year = self.current_time.strftime("%b %d %Y")
#         date = f"{day_of_week} {month_date_year}"
#         return date
#
#     def get_time_nl(self):
#         """"""
#         time = self.current_time.strftime('%I:%M %p').lower()
#         return time
#
#     def get_formatted_date_time(self):
#         """"""
#         date_in_nl = self.get_date_nl()
#         time_in_nl = self.get_time_nl()
#         formatted_date_time = f"{date_in_nl} {time_in_nl}"
#         return formatted_date_time
#
#     def get_date(self):
#         """"""
#         return self.current_time.date()
#
#     def set_time(self, hour, minute):
#         """"""
#         self.current_time = self.current_time.replace(hour=hour, minute=minute)
#
#     def set_date(self, year, month, day):
#         """"""
#         self.current_time = self.current_time.replace(year=year, month=month, day=day)

class Time:
    def __init__(self):
        # 8:00
        now = datetime.now()
        self.current_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
        self.time_step = timedelta(minutes=15)

    def advance_time(self):
        """15"""
        self.current_time += self.time_step

    def get_current_time(self):
        """datetime"""
        return self.current_time

    def get_date_nl(self):
        date = self.current_time.strftime("%Y-%m-%d")
        return date

    def get_time_24h(self):
        """24"""
        time = self.current_time.strftime('%H:%M')
        return time

    def get_formatted_date_time(self):
        """24"""
        date_in_nl = self.get_date_nl()
        time_in_24h = self.get_time_24h()
        formatted_date_time = f"{date_in_nl} {time_in_24h}"
        return formatted_date_time

    def get_date(self):
        """"""
        return self.current_time.date()

    def get_date_str(self):
        """ 'YYYY-MM-DD' """
        return self.current_time.strftime('%Y-%m-%d')

    def set_time(self, new_time: time):
        """ time """
        self.current_time = self.current_time.replace(hour=new_time.hour, minute=new_time.minute)


    def set_date(self, year, month, day):
        """"""
        self.current_time = self.current_time.replace(year=year, month=month, day=day)

    def calculate_future_date(self, day: int):
        """ day  day  'YYYY-MM-DD' """
        future_date = self.current_time + timedelta(days=day - 1)  # day=1 
        return future_date.strftime('%Y-%m-%d')



# print(t.get_date_nl())  # Tuesday Jul 23 2024
# print(t.get_time_nl())  # 06:00 am
# print(t.get_formatted_date_time())  # Tuesday Jul 23 2024 06:00 am
