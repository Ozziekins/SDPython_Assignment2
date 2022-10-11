class Console:
    def __init__(self, actions: list):
        self._message = 'Choose one operation from below :' \
                        ' 1 : Add classroom or Auditorium to institution' \
                        ' 2 : Print institution summary' \
                        ' 3 : Assign activity to classroom' \
                        ' 4 : Assign activity to LectureAuditorium' \
                        ' 5 : Dump University data' \
                        ' 6 : Exit program'
        self._institutions = []
        self.actions = actions

    def choose_action(self):
        print(self._message)
        try:
            choice = int(input())
            self.actions[choice].execute(self._institutions)
        except ValueError:
            print('Incorrect choice input. Please, try again!')

    def __str__(self):
        return self._message
