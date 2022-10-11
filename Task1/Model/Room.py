from Task1.Model.Activity import Activity
from Task1.Exceptions import ActivitiesOverlapException


class Room:
    def __init__(self, edu_name: str, number: str, capacity: int, air_cond: bool):
        self._edu_name = edu_name
        self._number = number
        self._capacity = capacity
        self._air_cond = air_cond
        self._activities = []

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

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

    def num_activities(self):
        return len(self._activities)

    def add_activity(self, activity: Activity):
        overlapping = list(map(lambda x: activity.not_overlaps(x), self._activities))
        # print(all(overlapping))
        # print(overlapping)
        if not all(overlapping):
            # Getting list of overlapping activities
            ov = [str(act) for i, act in enumerate(self._activities) if not overlapping[i]]
            # Raising an exception
            raise ActivitiesOverlapException('Activity conflicts with the following activities:\n' + '\n'.join(ov))
        else:
            self._activities.append(activity)

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
        return f'Lecture Auditorium ' + super(LectureAuditorium, self).__str__()


class Klassroom(Room):

    def __str__(self):
        return f'Klassroom ' + super().__str__()
