from datetime import datetime

from Exceptions import ActivityOutOfRangeException


class Activity:
    def __init__(self, name: str, start: datetime, end: datetime):
        if start.hour < 8 or end.hour > 21:
            raise ActivityOutOfRangeException("Activity should be during working hours! (8:00-21:00)")
        self._name = name
        self._start = start
        self._end = end

    def get_name(self):
        return self._name

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def not_overlaps(self, other):
        return False if self._start < other.get_end() and self._end > other.get_start() else True

    def __str__(self):
        return f'Activity(name: {self._name}, start: {self._start}, end: {self._end})'
