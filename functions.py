"""
This module contains custom filter for handlers and Analyzer classes
"""
import os
import datetime
from typing import List, Union

from pyrogram import filters
from pyrogram.types import CallbackQuery


# Custom callback_query data filter cause there is no official one
def dynamic_data_filter(data: Union[str, list]) -> filters.Filter:
    """
    Filter filters callback query's data.

    Parameters:
        data (``str`` | ``list[str]``):
            Data associated with the callback button.
    """
    async def func(flt, _, query: CallbackQuery):
        if isinstance(flt.data, list):
            for data in flt.data:
                if data == query.data:
                    return True
                else:
                    continue
            return False
        else:
            return flt.data == query.data

    return filters.create(func, data=data)

class Analyzer:
    __period_values = {
        "day": 1,
        "yesterday" : 2,
        "week" : 7,
        "month" : 28
    }
    __query_dict = {
        "tiktok" : "tiktok_download",
        "spotify" : "spotify_downloader",
        "youtube" : "youtube_download",
        "instagram" : "instagram_handler"
    }
    def __init__(self, query=None) -> None:
        self.value = None
        if query: query = Analyzer.__query_dict[query] #TODO: add queries dictionary
        self.query = query
    def get_info_per_period(self, period: str):
        period = Analyzer.__period_values[period]
        print(os.getcwd())
        if period != 2:
            with open(os.path.join("logs", "temp.log")) as file:
                for line in file:
                    stats = line.strip().split(" - ")
                    self._proccess_value(stats)
        for delta in range(1, period):
            date = str(datetime.date.today() - datetime.timedelta(days=delta))
            path = os.path.join("logs", date + ".log")
            if not os.path.exists(path):
                continue
            with open(path) as file:
                for line in file:
                    stats = line.strip().split(" - ")
                    self._proccess_value(stats)
        
        return self._proccess_result()
    def _proccess_value(self, stats: List[str]):
        ...
    def _proccess_result(self):
        if self.value:
            return self.value
        else:
            return 0
    @staticmethod
    def get_analyzer(stats_type: str, query_type: str = None) -> "Analyzer":
        if stats_type == "users":
            return UserAnalyzer()
        elif stats_type == "updates":
            return QueriesAnalyzer(query_type)
        elif stats_type == "successes":
            return SuccessesAnalyzer(query_type)

class UserAnalyzer(Analyzer):
    def _proccess_value(self, stats: List[str]):
        if not self.value:
            self.value = set()
        self.value.add(stats[2])
    def _proccess_result(self):
        #print(f"Im here and value is {self.value}")
        if not self.value:
            return 0
        return len(self.value)

class QueriesAnalyzer(Analyzer):
    def _proccess_value(self, stats: List[str]):
        if not self.value: self.value = 0
        if stats[3] == self.query: self.value += 1

class SuccessesAnalyzer(Analyzer):
    def _proccess_value(self, stats: List[str]):
        if not self.value: self.value = [0, 0]
        if stats[3] == self.query:
            if stats[-1] == "SUCCESS":
                self.value[0] += 1
            if stats[-1] != "UNKNOWN": self.value[1] += 1
    def _proccess_result(self):
        if not self.value: self.value = [0, 0]
        if not self.value[1]: return f"ratio - 1.00\nTotal number - 0"
        return f"ratio - {self.value[0] / self.value[1]:.2f}\nTotal number - {self.value[1]}"
