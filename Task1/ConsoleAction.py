import sys
from datetime import time
import jsonpickle

from Exceptions import UniversityNotFoundException, ActivitiesOverlapException, ActivityOutOfRangeException
from Task1.Model.EdInstitution import EdInstitution
from Utils import get_institution, print_summary
from Model.Room import Klassroom, LectureAuditorium
from Model.Activity import Activity
import re


class ConsoleAction:
    def execute(self, institutions: list[EdInstitution]) -> None:
        pass


class AddAuditorium(ConsoleAction):
    def execute(self, institutions: list[EdInstitution]) -> None:
        """
        Adds a LecturAuditorium or a Klassroom to a university
        :param institutions: list[EdInstitution] - list of Institutions
        """
        try:
            print("Enter institution name :")
            inst = get_institution(institutions)
            print("Enter (classroom - 1 or Auditorium - 2):")
            choice = int(input())
            if choice < 1 or choice > 2:
                raise ValueError
            print("Enter (capacity, number, air conditioner- yes/no):")
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



work_start = time.fromisoformat("06:00")
work_finish =time.fromisoformat("21:00")

class AddActivityKlassRoom(ConsoleAction):

    def execute(self, institutions):
        try:

            print("Enter institution name :")
            inst = get_institution(institutions)


            print("enter the desired klassroom number :")
            activity_room = str(input())

            k_room= inst.get_klassroom(activity_room)

            print("enter activity name:")
            activity_name = str(input())

            print("Enter the slot that you desire in format HH:MM - HH:MM :")
            slot = re.findall("\d\d[:]\d\d", input())



            start_slot = time.fromisoformat(slot[0])
            finish_slot = time.fromisoformat(slot[1])




            activity = Activity(name=activity_name, room=k_room.get_number(), start=start_slot, end=finish_slot)


            k_room.add_activity(activity)

            print(f"Successfully added activity to Klassroom from {start_slot} to {finish_slot} ")

        except (ActivityOutOfRangeException) as out_of_range:
            print(repr(out_of_range))
        except(ActivitiesOverlapException) as overlap:
            print(repr(overlap))
        except (UniversityNotFoundException) as not_found:
            print(repr(not_found))



class AddActivityAuditorium(ConsoleAction):
    def execute(self, institutions):
        try:

            print("Enter institution name :")
            inst = get_institution(institutions)

            print("enter the desired Auditorium number :")
            activity_auditorium = str(input())

            aud_room= inst.get_auditorium(activity_auditorium)

            print("enter activity name:")
            activity_name = str(input())

            print("Enter the slot that you desire in format HH:MM - HH:MM :")
            slot = re.findall("\d\d[:]\d\d", input())
            start_slot = time.fromisoformat(slot[0])
            finish_slot = time.fromisoformat(slot[1])

            activity = Activity(name=activity_name, room=aud_room.get_number(), start=start_slot, end=finish_slot)

            aud_room.add_activity(activity)

            print(f"Successfully added activity to Klassroom from {start_slot} to {finish_slot} ")



        except (ActivityOutOfRangeException) as out_of_range:

            print(repr(out_of_range))

        except(ActivitiesOverlapException) as overlap:

            print(repr(overlap))

        except (UniversityNotFoundException) as not_found:

            print(repr(not_found))


class Dump(ConsoleAction):
    def execute(self, institutions: list[EdInstitution]) -> None:
        """
        Dumps or loads institutions
        :param institutions: list[EdInstitution] - list of Institutions
        """
        try:
            print("Enter (1 - save universities, 2 - load university)")
            choice = int(input())
            if choice < 1 or choice > 2:
                raise ValueError
            if choice == 1:
                for i in institutions:
                    i.save_to_file()
            else:
                print("Enter file name:")
                name = str(input())
                print(name)
                with open(name, 'r') as file:
                    f = file.read()
                    institutions.append(jsonpickle.decode(f))
            print('Successfully saved!')
        except (ValueError, FileNotFoundError, Exception):
            print('Incorrect choice input. Please, try again!')


class PrintSummary(ConsoleAction):
    def execute(self, institutions: list[EdInstitution]) -> None:
        """
        Prints summary for institutions
        :param institutions: list[EdInstitution] - list of Institutions
        """
        print_summary(institutions)


class Exit(ConsoleAction):
    def execute(self, institutions: list[EdInstitution]) -> None:
        """
        Prints summary and exists the program
        :param institutions: list[EdInstitution] - list of Institutions
        """
        print_summary(institutions)
        sys.exit()
