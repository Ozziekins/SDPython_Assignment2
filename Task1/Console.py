from ConsoleAction import ConsoleAction
from Model.EdInstitution import EdInstitution


class Console:
    def __init__(self, actions: list[ConsoleAction], institutons: list[EdInstitution] = None):
        self._message = 'Choose one operation from below :\n' \
                        ' 1 : Add classroom or Auditorium to institution\n' \
                        ' 2 : Print institution summary\n' \
                        ' 3 : Assign activity to classroom\n' \
                        ' 4 : Assign activity to LectureAuditorium\n' \
                        ' 5 : Dump University data\n' \
                        ' 6 : Exit program\n'
        self._institutions = institutons if institutons else list()
        self._actions = actions

    def choose_action(self):
        print(self._message)
        try:
            choice = int(input()) - 1
            if choice < 0 or choice > 5:
                raise ValueError
            self._actions[choice].execute(self._institutions)
        except ValueError:
            print('Incorrect choice input. Please, try again!\n')

    def __str__(self):
        return self._message
