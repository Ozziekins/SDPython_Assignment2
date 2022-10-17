from threading import Thread

from src.Task2.test import get_data
from src.Task2.ui import begin
import shutup
shutup.please()

if __name__ == "__main__":
    th = Thread(target=get_data, daemon=True)

    # function is running on the main thread
    begin()
    th.start()
    th.join()
