from datetime import timedelta
from drive_service import get_file_id


class Files(object):
    """
    An iterator for getting file ids based on their name
    arranged by date.
    """
    def __init__(self, start_date):
        self.startDate = start_date
        self.currentDate = None

    def __iter__(self):
        return FileIterator(self)

    def get_date(self):
        if self.currentDate is None:
            self.currentDate = self.startDate
        else:
            self.currentDate = self.currentDate + timedelta(days=1)
        return get_file_id(self.currentDate.strftime("raw_%Y_%m_%d.csv"))


class FileIterator(object):
    def __init__(self, container):
        self.container = container

    def __next__(self):
        return self.container.get_date()
