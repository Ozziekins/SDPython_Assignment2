from Exceptions import UniversityNotFoundException
from Model import EdInstitution


def get_institution(institutions: list[EdInstitution]) -> EdInstitution:
    """
    Gets institution with the name from the cmd
    :param institutions: list[EdInstitution] - list of Institutions
    """
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
    """
    Prints summary for the list of institutions
    :param institutions: list[EdInstitution] - list of Institutions 
    """
    str_inst = [str(i) for i in institutions]
    print('\n\n'.join(str_inst) + '\n\n')
