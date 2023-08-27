import os
import datetime
from typing import List
from config import config

class Analyzer:
    __period_values = {
        "day": 1,
        "yesterday" : 2,
        "week" : 7,
        "month" : 28
    }
    def __init__(self, query=None) -> None:
        self.value = None
        if query: self.query = query
        
    def get_info_per_period(self, period: str):
        period = Analyzer.__period_values[period]
        print(os.getcwd())
        if period != 2:
            with open(os.path.join(config.logs_path, "temp.log")) as file:
                for line in file:
                    stats = line.strip().split(" - ")
                    self._proccess_value(stats)
        for delta in range(1, period):
            date = str(datetime.date.today() - datetime.timedelta(days=delta))
            path = os.path.join(config.logs_path, date + ".log")
            if not os.path.exists(path):
                continue
            with open(path) as file:
                for line in file:
                    stats = line.strip().split(" - ")
                    if stats[1] == "[WARNING]": continue
                    self._proccess_value(stats)
        
        return self._proccess_result()
    def _proccess_value(self, stats: List[str]):
        pass

    def _proccess_result(self):
        if self.value:
            return self.value
        else:
            return 0
    @staticmethod
    def get_analyzer(stats_type: str, query_type: str = None) -> "Analyzer":
        if stats_type == "users":
            return UserAnalyzer(query_type)
        elif stats_type == "updates":
            return QueriesAnalyzer(query_type)

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
