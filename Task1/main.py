from Console import Console
from ConsoleAction import *
from Model.EdInstitution import EdInstitution

if __name__ == '__main__':
    innopolis = EdInstitution('Innopolis University')
    auditorium = LectureAuditorium('KFU', '494', 120, False)
    klassRoom = Klassroom('KFU', '494', 120, True)
    klassRoom2 = Klassroom('KFU', '594', 120, True)
    activity = Activity("sas", '494', time.fromisoformat("10:30"), time.fromisoformat("11:30"))
    activity2 = Activity("sas", '494', time.fromisoformat("14:30"), time.fromisoformat("15:30"))
    activity3 = Activity("sas", '494', time.fromisoformat("10:30"), time.fromisoformat("11:30"))
    auditorium.add_activity(activity)
    auditorium.add_activity(activity2)
    klassRoom.add_activity(activity3)
    kfu = EdInstitution('KFU')
    kfu.add_auditorium(auditorium)
    kfu.add_kroom(klassRoom)
    kfu.add_kroom(klassRoom2)
    institutions = [innopolis, kfu]
    actions = [AddAuditorium(), PrintSummary(), AddActivityKlassRoom(), AddActivityAuditorium(), Dump(), Exit()]
    console = Console(actions, institutions)

    while True:
        console.choose_action()
