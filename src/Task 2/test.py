from datetime import datetime
from Services.Files import Files
from SqlProvider import SqlProvider
from sqlalchemy.orm import sessionmaker
import pandas as pd
from ML.DurationTrainer import DurationTrainer, DurationPredict
from Models import LoadedDay
from time import perf_counter, sleep
from ML.stream_quality import QualityPredictor
from threading import Thread


def train_model(data):
    agg = {
        'timestamp': ['min', 'max'],
        'dropped_frames': ['min', 'mean'],
        'FPS': ['min', 'max', 'mean', 'std'],
        'RTT': ['min', 'max', 'mean', 'std'],
        'bitrate': ['min', 'max', 'mean', 'std']
    }
    aggregate_df = data.groupby(['client_user_id', 'session_id'], as_index=False).agg(agg)
    aggregate_df.columns = ['client_user_id', 'session_id', 'session_start', 'session_end', 'dropped_frames_min',
                            'dropped_frames_mean', 'FPS_min', 'FPS_max', 'FPS_mean', 'FPS_std', 'RTT_min', 'RTT_max',
                            'RTT_mean', 'RTT_std', 'bitrate_min', 'bitrate_max', 'bitrate_mean', 'bitrate_std']
    aggregate_df['duration'] = (aggregate_df['session_end'] - aggregate_df['session_start']).dt.seconds
    DurationTrainer().train(
        aggregate_df.drop(['client_user_id', 'session_id', 'session_start', 'session_end'], axis=1))


def get_data():
    sql_provider = SqlProvider()
    sql_provider.create_tables()
    start_date = datetime(2022, 9, 2)
    sim = Files(start_date)
    for file_date, file_id in sim:
        time_start = perf_counter()
        if file_id is not None:
            download_url = f"https://drive.google.com/uc?id={'1GdUmvOH0eZu8bBYujTzpWuyCF9KHwnB7'}"
            df = pd.read_csv(download_url, index_col=False, parse_dates=['timestamp'])
            df.to_sql('Entries', con=sql_provider.engine, if_exists='append', index=False)
            loaded_day = LoadedDay(file_date=file_date, fetch_date=datetime.today())
            Session = sessionmaker(sql_provider.engine)
            with Session() as session:
                session.add(loaded_day)
                session.commit()
                train_model(df)
                loaded_day.train_date = datetime.today()
                session.commit()
        time_end = perf_counter()
        if (time_end - time_start) > 300:
            sleep(time_end - time_start - 300)


def first():
    input("Enter user id")
    test = pd.DataFrame(data=[
        [-0.938268, -0.524444, 0.244128, -0.089892, -0.089892, -0.017157, -0.015607, 12, -0.524444, 0.244128, -0.089892,
         -0.017157, -0.015607, 12]],
        columns=['dropped_frames_min',
                 'dropped_frames_mean',
                 'FPS_min',
                 'FPS_max',
                 'FPS_mean',
                 'FPS_std',
                 'RTT_min',
                 'RTT_max',
                 'RTT_mean',
                 'RTT_std',
                 'bitrate_min',
                 'bitrate_max',
                 'bitrate_mean',
                 'bitrate_std'])
    print(test.shape)
    print(DurationPredict(test))


t1 = Thread(target=first)
t2 = Thread(target=get_data)
t1.start()
t2.start()
t1.join()
t2.join()
