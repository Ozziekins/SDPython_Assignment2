import json

from Task1.Model.Room import Klassroom
from Task1.Model.Room import LectureAuditorium
import jsonpickle


class EdInstitution:
    def __init__(self, name: str, klassrooms: set[Klassroom] = None, auditoriums: set[LectureAuditorium] = None):
        if klassrooms is None:
            klassrooms = set()
        if auditoriums is None:
            auditoriums = set()
        self._name = name
        self._klassrooms = klassrooms if klassrooms else set()
        self._auditoriums = auditoriums if auditoriums else set()

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
        with open(f'{self._name}.json', 'w') as file:
            file.write(jsonpickle.encode(self, indent=4))

    # def __dict__(self):
    #     auds = [a.__dict__() for a in self._auditoriums]
    #     klass = [k.__dict__() for k in self._klassrooms]
    #     return {"name": self._name, "auditoriums": auds, "klassrooms": klass}

    def __str__(self):
        return f'{self._name}' + \
               f'\n\tclassroom(s) : {len(self._klassrooms)}' + \
               f'\n\tAuditorium(s): {len(self._auditoriums)}' + \
               f'\n\tStatus for today (now) : {self._available_krooms()} available classroom(s) and {self._available_auds()}'
