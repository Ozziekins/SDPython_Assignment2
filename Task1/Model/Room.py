from Task1.Model.Activity import Activity
from Task1.Exceptions import ActivitiesOverlapException, ActivityOutOfRangeException
from datetime import datetime


class Room:
    def __init__(self, edu_name: str, number: str, capacity: int, air_cond: bool):
        self._edu_name = edu_name
        self._number = number
        self._capacity = capacity
        self._air_cond = air_cond
        self._activities = []

    def get_edu_name(self):
        return self._edu_name

    def get_number(self):
        return self._number

    def set_number(self, number: str):
        self._number = number

    def get_capacity(self):
        return self._capacity

    def set_capacity(self, capacity: str):
        self._capacity = capacity

    def get_air_cond(self):
        return self._air_cond

    def set_air_cond(self, air_cond: bool):
        self._air_cond = air_cond

    def is_conditioned(self):
        return 'Yes' if self._air_cond else 'No'

    def _overlapping(self, other):
        return list(filter(lambda x: other.overlaps(x), self._activities))

    def is_available(self):
        try:
            act = Activity("", "", datetime.now(), datetime.now())
            return len(self._overlapping(act)) == 0
        except ActivityOutOfRangeException:
            return False

    def num_activities(self):
        return len(self._activities)

    def add_activity(self, activity: Activity):
        overlapping = self._overlapping(activity)
        # print(all(overlapping))
        # print(overlapping)
        if len(overlapping) != 0:
            # Getting list of overlapping activities
            ov = [str(act) for act in overlapping]
            # Raising an exception
            raise ActivitiesOverlapException('Activity conflicts with the following activities:\n' + '\n'.join(ov))
        else:
            self._activities.append(activity)

    def dump(self):
        acts = str([a.dump() for a in self._activities])
        return f'(edu_name:{self._edu_name}, number: {self._number}, capacity: {self._capacity}, air_cond: {self._air_cond}, activities: {acts})'

    def __str__(self):
        return f'{self._number}.\n' \
               f'Status:\n' \
               f' Capacity:{self._capacity}\n' \
               f' Air conditioning: {self.is_conditioned()}\n' \
               f' Number of activities: {self.num_activities()}'

    def __hash__(self):
        return int(self._number)


class LectureAuditorium(Room):

    def __str__(self):
        return f'Lecture Auditorium ' + super().__str__()


class Klassroom(Room):

    def __str__(self):
        return f'Klassroom ' + super().__str__()
