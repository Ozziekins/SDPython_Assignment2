from datetime import datetime, timedelta
from Services.Files import Files
from SqlProvider import SqlProvider
from sqlalchemy.orm import sessionmaker
import pandas as pd
from ML.DurationTrainer import DurationTrainer
from Models import LoadedDay
from time import perf_counter, sleep
from sqlalchemy import desc, func
from ML.stream_quality import QualityPredictor
from threading import Thread
import pandas as pd
from urllib.request import Request, urlopen


def aggregate_data(data):
    agg = {
        'timestamp': ['min', 'max', 'size'],
        'dropped_frames': ['min', 'max', 'mean', 'std'],
        'FPS': ['min', 'max', 'mean', 'std'],
        'RTT': ['min', 'max', 'mean', 'std'],
        'bitrate': ['min', 'max', 'mean', 'std'],
        'device': lambda x: pd.Series.mode(x)
    }
    aggregate_df = data.groupby(['client_user_id', 'session_id'], as_index=False).agg(agg)
    aggregate_df.columns = ['client_user_id', 'session_id', 'session_start', 'session_end', 'count', 'dropped_frames_min',
                            'dropped_frames_max', 'dropped_frames_mean', 'dropped_frames_std',
                            'FPS_min', 'FPS_max', 'FPS_mean', 'FPS_std', 'RTT_min', 'RTT_max',
                            'RTT_mean', 'RTT_std', 'bitrate_min', 'bitrate_max', 'bitrate_mean', 'bitrate_std',
                            'device']
    aggregate_df['duration'] = (aggregate_df['session_end'] - aggregate_df['session_start']).dt.seconds
    return aggregate_df


def get_data():
    interval = 60
    sql_provider = SqlProvider()
    sql_provider.create_tables()
    Session = sessionmaker(sql_provider.engine)
    with Session() as session:
        subquery = session.query(func.max(LoadedDay.train_date))
        qry = session.query(LoadedDay).filter(LoadedDay.train_date == subquery).first()
        if qry is not None:
            start_date = qry.file_date + timedelta(days=1)
        else:
            start_date = datetime(2022, 9, 2)
        sim = Files(start_date)
        for file_date, file_id in sim:
            time_start = perf_counter()
            if file_id is not None:
                req = Request(f"https://drive.google.com/uc?id={file_id}")
                req.add_header('User-Agent',
                               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
                content = urlopen(req)
                loaded_day = session.query(LoadedDay).filter(LoadedDay.file_date == file_date).first()
                df = pd.read_csv(content, index_col=False, parse_dates=['timestamp'])
                df = aggregate_data(df)
                if loaded_day is None:
                    df.to_sql('AggregateEntries', con=sql_provider.engine, if_exists='append', index=False)
                    loaded_day = LoadedDay(file_date=file_date, fetch_date=datetime.today())
                    session.add(loaded_day)
                    session.commit()
                DurationTrainer().train(
                    df.drop(['client_user_id', 'session_id', 'session_start', 'dropped_frames_std', 'dropped_frames_max',
                             'session_end',  'device', 'count'], axis=1))
                loaded_day.train_date = datetime.today()
                session.commit()
            time_end = perf_counter()
            if (time_end - time_start) < interval:
                sleep(interval - (time_end - time_start))


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
    print(DurationTrainer().predict(test))


t1 = Thread(target=first)
t2 = Thread(target=get_data)
t1.start()
t2.start()
t1.join()
t2.join()
