from Model.Activity import Activity
from Exceptions import ActivitiesOverlapException, ActivityOutOfRangeException
from datetime import  datetime


class Room:
    def __init__(self, edu_name: str, number: str, capacity: int, air_cond: bool, activities: list[Activity] = None):
        self._edu_name = edu_name
        self._number = number
        self._capacity = capacity
        self._air_cond = air_cond
        self._activities = activities if activities else list()

    def get_edu_name(self) -> str:
        return self._edu_name

    def get_number(self) -> str:
        return self._number

    def set_number(self, number: str) -> None:
        self._number = number

    def get_capacity(self) -> int:
        return self._capacity

    def set_capacity(self, capacity: int) -> None:
        self._capacity = capacity

    def get_air_cond(self) -> bool:
        return self._air_cond

    def set_air_cond(self, air_cond: bool) -> None:
        self._air_cond = air_cond

    def is_conditioned(self) -> str:
        return 'Yes' if self._air_cond else 'No'

    def _overlapping(self, other: Activity) -> list[Activity]:
        return list(filter(lambda x: other.overlaps(x), self._activities))

    def is_available(self) -> bool:
        """
        Checks if the room is available
        :return: bool; is available?
        """
        try:
            act = Activity("", "", datetime.now().time(), datetime.now().time())
            return len(self._overlapping(act)) == 0
        except ActivityOutOfRangeException:
            return False

    def num_activities(self) -> int:
        """
        Returns number of activities assigned to the room
        :return: int; number of activities
        """
        return len(self._activities)

    def add_activity(self, activity: Activity) -> None:
        """
        Adding an activity to the room
        :param activity: Activity; activity to add
        """
        # Getting overlapping activities
        overlapping = self._overlapping(activity)
        if len(overlapping) != 0:
            # Converting overlapping to string for execption to print
            ov = [str(act) for act in overlapping]
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
        return f'Lecture Auditorium ' + super().__str__()


class Klassroom(Room):

    def __str__(self):
        return f'Klassroom ' + super().__str__()
