from datetime import datetime

from Task1.Exceptions import ActivityOutOfRangeException


class Activity:
    def __init__(self, name: str, room: str, start: datetime, end: datetime):
        if start.hour < 8 or end.hour > 21:
            raise ActivityOutOfRangeException("Activity should be during working hours! (8:00-21:00)")
        self._room = room
        self._name = name
        self._start = start
        self._end = end

    def get_name(self) -> str:
        return self._name

    def get_start(self) -> datetime:
        return self._start

    def get_end(self) -> datetime:
        return self._end

    def overlaps(self, other) -> bool:
        return self._start < other.get_end() and self._end > other.get_start()

    def __str__(self):
        return f'Activity(name: {self._name}, start: {self._start}, end: {self._end})'
