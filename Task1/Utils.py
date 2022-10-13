from Exceptions import UniversityNotFoundException
from Model import EdInstitution


def get_institution(institutions: list[EdInstitution]) -> EdInstitution:
    name = str(input())

    inst = None
    for i in institutions:
        if i.get_name() == name:
            inst = i

    if inst:
        return inst
    else:
        raise UniversityNotFoundException(f'University with the name {name} not found!')


def print_summary(institutions: list[EdInstitution]):
    str_inst = [str(i) for i in institutions]
    print('\n\n'.join(str_inst) + '\n\n')
