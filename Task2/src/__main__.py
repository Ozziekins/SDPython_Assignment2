from threading import Thread
from ui import begin
from fetch import get_data

import shutup
shutup.please()

if __name__ == "__main__":
    th = Thread(target=get_data, daemon=True)
    th.start()
    # function is running on the main thread
    begin()
    th.join()
