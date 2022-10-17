from Task1.Console import Console
from Task1.ConsoleAction import *
from Task1.Model.EdInstitution import EdInstitution

if __name__ == '__main__':
    # innopolis = EdInstitution('Innopolis University')
    # auditorium = LectureAuditorium('KFU', '494', 120, False)
    # activity = Activity("sas", '494', time.fromisoformat("10:30"), time.fromisoformat("11:30"))
    # auditorium.add_activity(activity)
    # kfu = EdInstitution('KFU')
    # kfu.add_auditorium(auditorium)
    # institutions = [innopolis, kfu]
    # actions = [AddAuditorium(), PrintSummary(), AddActivityKlassRoom(), AddActivityAuditorium(), Dump(), Exit()]
    # console = Console(actions, institutions)
    #
    # while True:
    #     console.choose_action()

    act = Activity("sas", '494', time.fromisoformat("10:30"), time.fromisoformat("11:30"))
    act2 = Activity("sas", '494', time.fromisoformat("10:30"), time.fromisoformat("11:30"))

    auditorium = LectureAuditorium('KFU', '494', 120, False)
    auditorium.add_activity(act)

    innopolis = EdInstitution('Innopolis University')

    innopolis.add_auditorium(auditorium)

    print(innopolis)
