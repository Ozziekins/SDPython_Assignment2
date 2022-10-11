from datetime import datetime
import time
from Files import Files
import pandas as pd
from SqlProvider import SqlProvider


sqlProvider = SqlProvider()
sqlProvider.create_tables()
start_date = datetime(2022, 9, 2)
sim = Files(start_date)

for file_id in sim:
    time.sleep(300)
    if id is not None:
        download_url = f"https://drive.google.com/uc?id={file_id}"
        df = pd.read_csv(download_url)
        df.to_sql('Entries', con=sqlProvider.engine, if_exists='append', index=False)
