import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from datetime import datetime, date, timedelta
from SqlProvider import SqlProvider
from ML.DurationTrainer import DurationTrainer
from ML.stream_quality import QualityPredictor

sqlProvider = SqlProvider()

Session = sessionmaker(bind=sqlProvider.engine)
session = Session()

def statsFor7Days():
    # if today is earlier than start day - 7days, then print just stats for all the days since start with a note
    df = pd.read_sql_query('select * from "AggregateEntries";', con=sqlProvider.engine)
    df["session_start"] = pd.to_datetime(df["session_start"])

    df.sort_values(by="session_start")
    df["just_date"] = df["session_start"].dt.date
    today = df["just_date"].iat[-1]
    week_prior = today - timedelta(weeks=1)
    first_day = date(2022, 9, 1)

    num_days = today - first_day

    if week_prior < first_day:
        print(f"It has only been {num_days} since we started our server. However, we will send the report for this period.")

    seven_day_df = df.loc[(df["just_date"] >= week_prior) & (df["just_date"] < today)]
    total_sessions = df["session_id"].count()

    df["duration"] = pd.to_timedelta(df["duration"], unit="s")

    average_time_per_session = round(df["duration"].mean() / pd.Timedelta("1 minute"), 2)

    sum_of_hours = round(df["duration"].sum() / pd.Timedelta("1 hour"), 2)

    summaryText = f"""Statistics for the past 7 days:
        Total sessions : {total_sessions} 
        Average time spent per session : {average_time_per_session} min
        Sum of hours spent by all users : {sum_of_hours} hours \n"""
    print(summaryText)

    return summaryText

def isSuperUser(userID, df):
    # a user who has sessions time more than 60 min in a week
    total_session = df["duration"].sum() / pd.Timedelta('1 minute')

    if total_session > 60:
        return "Yes"
    else:
        return "No"

def printUserSummary():
    # 07393db8-e059-4cbd-b16f-88ab2019f045
    userID = input("Enter user id: \n")

    df = pd.read_sql_query(f"""select * from public."AggregateEntries" where client_user_id='{userID}';""",
                           con=sqlProvider.engine)

    while True:
        if userID in set(df['client_user_id']):
            df["duration"] = pd.to_timedelta(df["duration"], unit="s")

            # df.query(f"client_user_id == '{userID}'", inplace=True)
            num_sessions = df["session_id"].count()

            df.sort_values(by="session_start")
            df["just_date"] = df["session_start"].dt.date
            first_session = df["just_date"].iat[0]

            average_per_session = round(df["duration"].mean() / pd.Timedelta('1 minute'), 2)

            df.sort_values(by="session_start", ascending=False)
            recent_session = df["just_date"].iat[0]

            most_device = df["device"].mode().values

            devices = df["device"].unique()

            num_bad_sessions = totalNumberOfBadSessions(userID, df)

            estimated_next_session_time = nextSessionDuration(userID)

            super_user = isSuperUser(userID, df)

            rtt = round(df["RTT_mean"].mean(), 3)
            fps = round(df["FPS_mean"].mean(), 3)
            dropped_frames = round(df["dropped_frames_mean"].mean(), 3)
            bitrate = round(df["bitrate_mean"].mean(), 3)

            # if no interval is given, then give entire summary of this user
            # interval = input("Enter period (yyyy/mm/dd - yyyy/mm/dd) : \n")

            print(f"""User found!!
                User with id : {userID}
                    Number of sessions : {num_sessions}
                    Date of first session : {first_session}
                    Average time spent per session : {average_per_session} minutes
                    Date of most recent session : {recent_session}
                    Most frequently used device : {most_device}
                    Devices used : {devices}
                    Average of : 1) Round trip time is {rtt} (RTT) 2) Frames per Second is {fps} 3) Dropped Frames is {dropped_frames} 4) bitrate is {bitrate}
                    Total number of bad sessions (predicted using ML model): {num_bad_sessions}
                    Estimated next session time : {estimated_next_session_time} hrs
                    Super user : {super_user}\n""")

            answer = input("Find another user ? (yes/no) \n")
            if answer == "yes":
                userID = input("Enter user id: \n")
                df = pd.read_sql_query(f"""select * from public."AggregateEntries" where client_user_id='{userID}';""",
                                       con=sqlProvider.engine)
            elif answer == "no":
                break
            else:
                print("Answer not recognized. Exiting\n")
                break
        else:
            print("User cannot be found")
            userID = input("Try again, Enter user id: \n")

# def printSessionSummary():
#     # b3aebc80-ff28-4569-bd18-2ace692f668e
#     sessionID = input("Enter session id: \n")


def predictNextSessionDuration():
    userID = input("Enter user id: \n")

    duration = nextSessionDuration(userID)

    print(f"The predicted session duration for user {userID} is {duration} \n")


def totalNumberOfBadSessions(userID, df):

    formatted_df = df[['FPS_mean', 'FPS_std', 'RTT_mean', 'RTT_std', 'dropped_frames_mean',
                            'dropped_frames_std', 'dropped_frames_max']]
    formatted_df = formatted_df.rename(columns={'FPS_mean': 'fps_mean', 'FPS_std': 'fps_std', 'RTT_mean': 'rtt_mean',
                                                'RTT_std': "rtt_std"})

    quality_predictor = QualityPredictor()

    df = formatted_df.apply(lambda x: quality_predictor.predict(x.to_frame().transpose()), axis=1)
    num = df.sum()

    return num


def nextSessionDuration(userID):

    df = pd.read_sql_query(f"""select * from public."AggregateEntries" where client_user_id='{userID}';""",
                           con=sqlProvider.engine)

    df_mean = df[["dropped_frames_min", "dropped_frames_mean", "FPS_min", "FPS_max", "FPS_mean", "FPS_std", "RTT_min",
                  "RTT_max", "RTT_mean", "RTT_std", "bitrate_min", "bitrate_max", "bitrate_mean", "bitrate_std"]].mean()

    duration = DurationTrainer().predict(df_mean.to_frame().transpose())

    next_session_duration = round(pd.to_timedelta(duration, unit="s") / pd.Timedelta("1 hour"), 2)

    return next_session_duration


def fetchAndUpdateData():
    df = pd.read_sql_query(f"""select * from public."LoadedDays";""", con=sqlProvider.engine)

    df["fetch_date"] = pd.to_datetime(df["fetch_date"])
    df["just_date"] = df["fetch_date"].dt.time

    interval = datetime.combine(date.today(), datetime.now().time()) - datetime.combine(date.today(), df["just_date"].iloc[-1])
    cond = interval / pd.Timedelta('1 minute')

    if int(cond < 5):
        print("Everything is up to date!\n")


def topFiveUsers():
    # query our db by time spent and return the 5rows
    df = pd.read_sql_query('select * from "AggregateEntries";', con=sqlProvider.engine)
    df["duration"] = pd.to_timedelta(df["duration"], unit="s")

    sessions_time = df.groupby(["client_user_id"])["duration"].agg(["sum"])
    sessions_time["days_spent_gaming"] = sessions_time["sum"].dt.components["days"]
    sessions_time["hours_spent_gaming"] = sessions_time["sum"].dt.components["hours"]
    sessions_time_total = sessions_time.sort_values(by="sum", ascending=False)
    sessions_time_total = sessions_time_total.drop(columns=["sum"])

    top_users = sessions_time_total.head(5)
    print("Top users are: \n", top_users, "\n")


def saveToFile(data, file_name):
    with open(file_name+".txt", "w") as f:
        f.write(data)


def exitSession():
    summaryText = statsFor7Days()

    saveSummary = input("Save summary ? (yes/no)\n")
    if saveSummary == "yes":
        saveToFile(summaryText, "summary")
    elif saveSummary == "no":
        pass
    else:
        saveSummary = input("Answer not recognized. Do you want to save the summary? (yes/no) ")


def begin():
    while True:
        choice = int(input("""Choose one operation from below :
            1 : Get status for the past 7 days
            2 : Print user summary 
            3 : Predict user next session duration
            4 : Fetch new data and update users data and ML model
            5 : Get top 5 users based on time spent gaming
            6 : Exit program \n"""))

        if choice == 1:
            statsFor7Days()
        elif choice == 2:
            printUserSummary()
        elif choice == 3:
            predictNextSessionDuration()
        elif choice == 4:
            fetchAndUpdateData()
        elif choice == 5:
            topFiveUsers()
        elif choice == 6:
            exitSession()
            break
        else:
            choice = int(input("Incorrect choice, try again \n"))


if __name__ == "__main__":
    begin()