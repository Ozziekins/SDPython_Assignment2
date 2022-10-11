import sys

from Exceptions import UniversityNotFoundException
from Utils import get_institution, print_summary
from Model.Room import Klassroom, LectureAuditorium
import re


class ConsoleAction:
    def execute(self, institutions):
        pass


class AddAuditorium(ConsoleAction):
    def execute(self, institutions: list):
        try:
            print("Enter institution name :")
            inst = get_institution(institutions)
            print("Enter (classroom - 1 or Auditorium - 2):")
            choice = int(input())
            print("Enter (capacity, number, air conditioner- yes/no):")
            # TODO: add a fine regexp here
            args = re.search("([1-9][0-9]+) ([0-9]+) (yes|no)", input())
            if not args:
                raise ValueError

            capacity, number, air_conditioner = int(args.group(1)), args.group(2), True if args.group(3) == 'yes' else False

            if choice == 1:
                k_room = Klassroom(inst.get_name(), number, capacity, air_conditioner)
                inst.add_kroom(k_room)
                print("Successfully added KlassRoom!")
            else:
                aud = LectureAuditorium(inst.get_name(), number, capacity, air_conditioner)
                inst.add_auditorium(aud)
                print("Successfully added LectureAuditorium!")

        except (UniversityNotFoundException, ValueError) as error:
            print(repr(error))


# class AddActivityKlassRoom(ConsoleAction):
#
# class AddActivityAuditorium(ConsoleAction):

class PrintSummary(ConsoleAction):
    def execute(self, institutions):
        print_summary(institutions)


class Exit(ConsoleAction):
    def execute(self, institutions):
        print_summary(institutions)
        sys.exit()
