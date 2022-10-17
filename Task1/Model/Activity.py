from datetime import time

from Exceptions import ActivityOutOfRangeException


class Activity:
    def __init__(self, name: str, room: str, start: time, end: time):
        if start.hour < 8 or end.hour > 21:
            raise ActivityOutOfRangeException("Activity should be during working hours! (8:00-21:00)")
        self._room = room
        self._name = name
        self._start = start
        self._end = end

    def get_name(self) -> str:
        return self._name

    def get_start(self) -> time:
        return self._start

    def get_end(self) -> time:
        return self._end

    def overlaps(self, other) -> bool:
        """
        Checks if two activities overlap
        :param other: Activity; other activity
        :return: bool; overlap or not?
        """
        return self._start < other.get_end() and self._end > other.get_start()

    def __str__(self):
        return f'Activity(name: {self._name}, start: {self._start}, end: {self._end})'
