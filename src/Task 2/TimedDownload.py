from datetime import timedelta

from drive_service import get_file_id


class Simulator(object):
    def __init__(self, start_date):
        self.startDate = start_date

    def __iter__(self):
        return SimulatorIterator(self)


class SimulatorIterator(object):
    def __init__(self, container):
        self.container = container
        self.currentDate = None

    def __next__(self):
        if self.currentDate is None:
            self.currentDate = self.container.startDate
        else:
            self.currentDate = self.currentDate + timedelta(days=1)
        return get_file_id(self.currentDate.strftime("raw_%Y_%m_%d.csv"))

    def __iter__(self):
        return self

