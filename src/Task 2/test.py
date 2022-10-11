from datetime import datetime
import time
from Files import Files
import pandas as pd

start_date = datetime(2022, 9, 2)
sim = Files(start_date)

for file_id in sim:
    time.sleep(60)
    if id is not None:
        download_url = f"https://drive.google.com/uc?id={file_id}"
        df = pd.read_csv(download_url)
        print(df.count())
