from Exceptions import RoomNotFoundException
from Model.Room import Klassroom, Room
from Model.Room import LectureAuditorium
import jsonpickle


class EdInstitution:
    def __init__(self, name: str, klassrooms: set[Klassroom] = None, auditoriums: set[LectureAuditorium] = None):
        self._name = name
        self._klassrooms = klassrooms if klassrooms else set()
        self._auditoriums = auditoriums if auditoriums else set()

    def get_name(self) -> str:
        return self._name

    def get_auditoriums(self) -> set[LectureAuditorium]:
        return self._auditoriums

    def get_krooms(self) -> set[Klassroom]:
        return self._klassrooms

    def get_room(self, number: str, auditorium: bool) -> Room:
        """
        Function to get a room from the university given a number
        :param number: str; number of room to fetch
        :param auditorium: bool; flag to choose from auditoriums or klassrooms
        :return:
        """
        room = None
        rooms = self._auditoriums if auditorium else self._klassrooms
        for r in rooms:
            if r.get_number() == number:
                room = r

        if room:
            return room
        else:
            raise RoomNotFoundException(f'Room number {number} not found')

    def get_auditorium(self, number: str) -> Room:
        return self.get_room(number, auditorium=True)

    def get_klassroom(self, number: str) -> Room:
        return self.get_room(number, auditorium=False)

    def add_kroom(self, k_room: Klassroom) -> None:
        """
        Adds klassrom to the EdInstitution
        :param k_room: KlassRoom; instance of Klassroom to add
        """

        self._klassrooms.add(k_room)

    def add_auditorium(self, aud: LectureAuditorium) -> None:
        """
        Adds auditorium to the university
        :param aud: LectureAuditorium; instance of LectureAuditorium to add
        """
        self._auditoriums.add(aud)

    def _remove(self, number: str, rooms: set[Room]) -> set[Room]:
        """
        Helper function to remove room (lecture or auditorium)
        :param number: str; number of room to delete
        :param rooms: set[Rooms]; rooms from which to delete one
        :return: set[Rooms]; rooms without removed one
        """
        to_del = None
        for room in rooms:
            if room.get_number() == number:
                to_del = room

        if to_del:
            rooms.remove(to_del)

        return rooms

    def remove_kroom(self, number: str) -> None:
        """
        Removes a KlassRoom from the set of Klassrooms, using auditorium number.
        If such KlassRoom is not found - does nothing
        :param number: str; Number of a Klassroom to remove
        """
        self._klassrooms = self._remove(number, self._klassrooms)

    def remove_auditorium(self, number: str) -> None:
        """
        Removes a LectureAuditorium from the set of LectureAuditoriums, using auditorium number.
        If such LectureAuditorium is not found - does nothing
        :param number: str, number of LectureAuditoriums to remove
        """
        self._auditoriums = self._remove(number, self._auditoriums)

    def _available_krooms(self) -> int:
        """
        Helper function to get how many klassrooms are available in university
        :return: int; number of available klassrooms
        """
        available = list(filter(lambda x: x.is_available(), self._klassrooms))
        return len(available)

    def _available_auds(self) -> int:
        """
        Helper function to get how many lectureAuditoriums are available in university
        :return: int; number of available lectureAuditoriums
        """
        available = list(filter(lambda x: x.is_available(), self._auditoriums))
        return len(available)

    def save_to_file(self) -> None:
        """
        Writes university to file {uni_name}.txt
        """
        with open(f'{self._name}.json', 'w') as file:
            file.write(jsonpickle.encode(self, indent=4))

    def __str__(self):
        return f'{self._name}' + \
               f'\n\tclassroom(s) : {len(self._klassrooms)}' + \
               f'\n\tAuditorium(s): {len(self._auditoriums)}' + \
               f'\n\tStatus for today (now) : {self._available_krooms()} available classroom(s) and {self._available_auds()} available auditorium(s)'
