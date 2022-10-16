class ActivitiesOverlapException(Exception):
    """
    Raised when activities overlap
    """


class ActivityOutOfRangeException(Exception):
    """
    Raised when activity is outside working hours
    """


class UniversityNotFoundException(Exception):
    """
    Raised when university provided is not found
    """


class RoomNotFoundException(Exception):
    """
    Raised when a room is not found
    """
