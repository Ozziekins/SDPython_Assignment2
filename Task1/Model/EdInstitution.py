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

    def __str__(self):
        klasses = '' if not self._klassrooms else 'Klassrooms:\n\n' + '\n'.join([str(kl) for kl in self._klassrooms])
        audits = '' if not self._auditoriums else 'LectureAuditoriums:\n\n' + '\n'.join([str(au) for au in self._auditoriums])
        return f'University - {self.name}\n' + klasses + '\n' + audits
