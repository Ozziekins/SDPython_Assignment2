from Task1.Console import Console
from Task1.ConsoleAction import *
from Task1.Model.EdInstitution import EdInstitution

if __name__ == '__main__':
    innopolis = EdInstitution('Innopolis University')
    kfu = EdInstitution('KFU')
    institutions = [innopolis, kfu]
    actions = [AddAuditorium(), Dump(), PrintSummary(), Exit()]
    console = Console(actions, institutions)

    while True:
        console.choose_action()
