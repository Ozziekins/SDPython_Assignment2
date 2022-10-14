from datetime import datetime
from Files import Files
from SqlProvider import SqlProvider
from sqlalchemy.orm import sessionmaker
import pandas as pd


sqlProvider = SqlProvider()
sqlProvider.create_tables()
start_date = datetime(2022, 9, 2)
sim = Files(start_date)

Session = sessionmaker(bind=sqlProvider.engine)
session = Session()


for file_id in sim:
    #time.sleep(300)
    if file_id is not None:
        download_url = f"https://drive.google.com/uc?id={file_id}"
        df = pd.read_csv(download_url)
        df.to_sql('Entries', con=sqlProvider.engine, if_exists='append', index=False)