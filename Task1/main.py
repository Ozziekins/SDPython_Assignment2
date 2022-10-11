from Model.Activity import Activity
from Model.Room import Klassroom
from Model.EdInstitution import EdInstitution
from datetime import datetime

if __name__ == '__main__':

    a = EdInstitution("Innopolis University")
    b = Klassroom("Innopolis University", "404", 140, True)

    d_format = "%d-%b-%Y-%H:%M"

    act = Activity("Activity 1", datetime.strptime("01-Apr-2012-08:00", d_format), datetime.strptime("01-Apr-2012-12:00", d_format))
    act2 = Activity("Activity 1", datetime.strptime("01-Apr-2012-15:00", d_format), datetime.strptime("01-Apr-2012-19:00", d_format))
    act3 = Activity("Activity 1", datetime.strptime("01-Apr-2012-09:00", d_format),
                    datetime.strptime("01-Apr-2012-17:00", d_format))

    b.add_activity(act)
    b.add_activity(act2)
    # b.add_activity(act3)

    # print(b)

    a.add_kroom(b)

    print(a)

    institutions = [EdInstitution("Innopolis University"), EdInstitution("KFU")]
    print(institutions[0])

    message = 'Choose one operation from below :' \
              ' 1 : Add classroom or Auditorium to institution' \
              ' 2 : Print institution summary' \
              ' 3 : Assign activity to classroom' \
              ' 4 : Assign activity to LectureAuditorium' \
              ' 5 : Exit program'
    #
    # while True:
    #     print(message)


