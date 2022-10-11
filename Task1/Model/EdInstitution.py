from Task1.Model.Room import Klassroom
from Task1.Model.Room import LectureAuditorium


class EdInstitution:
    def __init__(self, name: str):
        self._name = name
        self._klassrooms = set()
        self._auditoriums = set()

    def get_name(self):
        return self._name

    def add_kroom(self, k_room: Klassroom):
        """
        Adds klassrom to the EdInstitution
        :param k_room: KlassRoom; instance of Klassroom to add
        """

        self._klassrooms.add(k_room)

    def add_auditorium(self, aud: LectureAuditorium):
        """
        Adds auditorium to the university
        :param aud: LectureAuditorium; instance of LectureAuditorium to add
        """
        self._auditoriums.add(aud)

    def _remove(self, number: str, rooms: set):
        to_del = None
        for room in rooms:
            if room.get_number() == number:
                to_del = room

        if to_del:
            self._klassrooms.remove(to_del)

        return rooms

    def _available_krooms(self):
        available = list(filter(lambda x: x.is_available(), self._klassrooms))
        return len(available)

    def _available_auds(self):
        available = list(filter(lambda x: x.is_available(), self._auditoriums))
        return len(available)

    def remove_kroom(self, number: str):
        """
        Removes a KlassRoom from the set of Klassrooms, using auditorium number.
        If such KlassRoom is not found - does nothing
        :param number: str; Number of a Klassroom to remove
        """
        self._klassrooms = self._remove(number, self._klassrooms)

    def remove_auditorium(self, number: str):
        """
        Removes a LectureAuditorium from the set of LectureAuditoriums, using auditorium number.
        If such LectureAuditorium is not found - does nothing
        :param number: str, number of LectureAuditoriums to remove
        """
        self._auditoriums = self._remove(number, self._auditoriums)

    def save_to_file(self):
        classrooms = str([i.dump() for i in self._klassrooms])
        auditoriums = str([i.dump() for i in self._klassrooms])
        with open(f'{self._name}.txt', 'w') as f:
            f.write(f'EdInstitution(name: {self._name}, classrooms: {classrooms}, auditoriums: {auditoriums})')

    def __str__(self):
        return f'{self._name}' + \
               f'\n\tclassroom(s) : {len(self._klassrooms)}' + \
               f'\n\tAuditorium(s): {len(self._auditoriums)}' + \
               f'\n\tStatus for today (now) : {self._available_krooms()} available classroom(s) and {self._available_auds()} '
