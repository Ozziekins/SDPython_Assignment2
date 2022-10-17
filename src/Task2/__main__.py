from threading import Thread

from src.Task2.test import get_data
from src.Task2.ui import begin
import shutup
shutup.please()

if __name__ == "__main__":
    t1 = Thread(target=begin)
    t2 = Thread(target=get_data)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
